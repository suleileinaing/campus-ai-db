"""LLM-as-a-judge: 예측 SQL 의 실행 결과가 정답(gold)과 의미상 같은지 ChatKHU 로 1/0 판정한다.

execution match(compare.py)는 값을 글자 단위로 비교해서, 의미는 맞지만 형식이 다른 답(컬럼 구성,
'03' 과 3, 단위 표기 등)을 오답으로 처리한다. 이 모듈은 이미 돌린 평가 결과(results.jsonl)를 읽어
문항마다 [질문 + 정답 표 + 모델 답변(예측 SQL 실행 결과 표)] 을 judge 에 보내고, 두 기준을 나란히 저장한다.

  python -m text2sql.llm_judge --run exec100_zeroshot
  python -m text2sql.evaluate --gold ... --llm-judge          # 평가 직후 바로 채점
  → results/<run>/judge.jsonl, judge_compare.csv, judge_summary.md, judge_summary.json

- judge 모델은 CHATKHU_JUDGE_MODEL(없으면 CHATKHU_MODEL), temperature 0 으로 호출한다.
- 출력은 JSON 한 줄 {"verdict": 0|1, "reason": "..."} 로 고정하고, 형식이 틀리면 한 번 다시 요청한다.
- SQL 실행 실패·생성 API 오류 문항은 judge 를 부르지 않고 0 으로 둔다(답변이 없음).
- judge.jsonl 에 이미 판정된 문항은 다시 부르지 않는다(중단 후 이어서 실행). --force 로 전부 다시.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path

from .config import RESULTS_DIR, Settings
from .evaluate import _pct

MAX_ROWS = 30  # judge 에 보여줄 최대 행 수(정답은 최대 4행이지만 예측은 수백 행일 수 있음)
REASON_MAX = 200

JUDGE_SYSTEM = """너는 Text2SQL 평가 채점자다.
질문, 정답 표, 모델 답변(모델이 만든 SQL 을 실행한 결과 표)을 보고, 모델 답변이 질문에 대해 정답과 의미상 같은 정보를 주는지 판정한다.

판정 기준
- 1(정답): 질문이 묻는 핵심 값이 정답과 모두 일치한다. 다음 차이는 허용한다.
  컬럼 이름·순서, 질문과 관련된 추가 컬럼, 표기 차이(3 과 3.0, '03' 과 3, 단위·날짜 형식, 대소문자, 공백),
  질문이 순서를 요구하지 않을 때의 행 순서, 같은 정보를 다른 형태로 나타낸 경우(예: 여러 행 ↔ 쉼표로 이은 한 값).
- 0(오답): 핵심 값이 다르거나 빠졌다, 정답에 없는 행이 섞였거나 정답 행이 빠졌다,
  정답이 0행인데 모델이 행을 돌려줬다(또는 그 반대), 질문이 요구한 정보 중 일부만 줬다.
- 정답 표가 기준이다. 네 지식으로 정답을 고치거나 의심하지 마라.
- 표가 잘렸다고 표시된 경우, 보이는 행과 전체 행 수로 판단한다.

출력 형식: 다른 글 없이 JSON 한 줄만 출력한다.
{"verdict": 1 또는 0, "reason": "판정 이유 한국어 한 문장(80자 이내)"}"""

RETRY_MSG = '형식 오류. 다른 글 없이 {"verdict": 1 또는 0, "reason": "..."} JSON 한 줄만 다시 출력하라.'


@dataclass
class JudgeResult:
    verdict: int | None  # 1/0, 판정 실패면 None
    reason: str
    status: str  # judged / skipped:<사유> / parse_error / api_error
    raw: str = ""
    tokens: int = 0


def format_table(columns: list[str] | None, rows: list[list] | None, max_rows: int = MAX_ROWS) -> str:
    rows = rows or []
    if not rows:
        return "(0행)"
    names = list(columns or []) or [f"col{j + 1}" for j in range(len(rows[0]))]
    shown = [dict(zip(names, r)) for r in rows[:max_rows]]
    head = f"({len(rows)}행" + (f", 앞 {max_rows}행만 표시)" if len(rows) > max_rows else ")")
    return head + "\n" + json.dumps(shown, ensure_ascii=False, default=str)


def build_messages(rec: dict) -> list[dict]:
    order = "질문이 순서를 요구하므로 행 순서도 비교한다." if rec.get("ordered") else "행 순서는 비교하지 않는다."
    user = (
        f"질문: {rec['question']}\n\n"
        f"정답 {format_table(rec.get('gold_columns'), rec.get('gold_rows'))}\n\n"
        f"모델 답변 {format_table(rec.get('pred_columns'), rec.get('pred_rows'))}\n\n"
        f"({order})"
    )
    return [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]


def parse_verdict(text: str) -> tuple[int, str]:
    """judge 응답에서 {"verdict", "reason"} 을 꺼낸다. 형식이 틀리면 ValueError."""
    m = re.search(r"\{.*\}", text or "", flags=re.S)
    if not m:
        raise ValueError("JSON 객체가 없음")
    obj = json.loads(m.group(0))
    v = obj.get("verdict")
    if isinstance(v, str):
        v = v.strip()
    if v in (1, "1", True):
        verdict = 1
    elif v in (0, "0", False):
        verdict = 0
    else:
        raise ValueError(f"verdict 값이 0/1 이 아님: {v!r}")
    return verdict, str(obj.get("reason") or "").strip()[:REASON_MAX]


def skip_result(rec: dict) -> JudgeResult | None:
    """judge 를 부를 필요가 없는 문항(답변이 없거나 정답이 없음)."""
    if rec.get("strict") is None:
        return JudgeResult(None, "정답(gold) 오류로 채점 제외", "skipped:gold_invalid")
    if rec.get("api_error"):
        return JudgeResult(0, "SQL 생성 API 오류로 답변 없음", "skipped:api_error")
    if rec.get("expect_refusal"):  # 거부 문항은 거부 여부가 정답이므로 실행 비교 결과를 그대로 쓴다
        return JudgeResult(int(bool(rec["strict"])), f"거부 문항: {rec.get('diagnosis')}", "skipped:refusal")
    if not rec.get("exec_ok"):
        return JudgeResult(0, f"SQL 실행 실패({rec.get('exec_error_kind')})로 답변 없음", "skipped:exec_fail")
    return None


def judge_record(llm, rec: dict, max_retries: int = 1) -> JudgeResult:
    skipped = skip_result(rec)
    if skipped:
        return skipped
    messages = build_messages(rec)
    raw, tokens = "", 0
    for _ in range(max_retries + 1):
        try:
            resp = llm.complete(messages)
        except Exception as exc:  # 크레딧 부족·네트워크 등: 기록하고 다음 실행에서 다시 시도
            return JudgeResult(None, f"{type(exc).__name__}: {exc}"[:REASON_MAX], "api_error", raw, tokens)
        raw, tokens = resp.text, tokens + resp.prompt_tokens + resp.completion_tokens
        try:
            verdict, reason = parse_verdict(raw)
            return JudgeResult(verdict, reason, "judged", raw, tokens)
        except (ValueError, json.JSONDecodeError):
            messages = [*messages, {"role": "assistant", "content": raw}, {"role": "user", "content": RETRY_MSG}]
    return JudgeResult(None, "judge 응답 형식 오류", "parse_error", raw, tokens)


def agreement(exec_ok: bool | None, verdict: int | None) -> str:
    if exec_ok is None or verdict is None:
        return "n/a"
    if exec_ok and verdict:
        return "both_correct"
    if not exec_ok and not verdict:
        return "both_wrong"
    return "llm_only" if verdict else "exec_only"


AGREEMENT_DESC = {
    "llm_only": "실행 비교 X / LLM O — 형식 차이로 실행 비교가 놓친 정답인지 확인",
    "exec_only": "실행 비교 O / LLM X — judge 오판일 가능성이 큼",
}


def run_judge(out_dir: Path, llm, judge_model: str, force: bool = False) -> dict:
    src = out_dir / "results.jsonl"
    if not src.exists():
        raise SystemExit(f"{src} 가 없습니다. 먼저 evaluate 를 돌리세요.")
    records = [json.loads(line) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]

    log_path = out_dir / "judge.jsonl"
    done: dict[str, dict] = {}
    if log_path.exists() and not force:
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                j = json.loads(line)
                # 판정이 끝났고 같은 judge 일 때만 재사용(뒤에 적힌 줄이 앞 줄을 덮음)
                if j.get("llm_verdict") is not None and j.get("judge_model") == judge_model:
                    done[j["id"]] = j
    elif log_path.exists():
        log_path.unlink()

    rows = []
    # 새 판정은 한 줄씩 덧붙여서 중간에 끊겨도 다음 실행이 이어받게 하고, 끝나면 문항 순서대로 다시 쓴다
    with log_path.open("a", encoding="utf-8") as log:
        for idx, rec in enumerate(records, 1):
            prev = done.get(rec["id"])
            if prev and prev.get("pred_sql") == rec.get("pred_sql"):
                row, tag = prev, "(이전 판정)"
            else:
                jr = judge_record(llm, rec)
                row = {
                    "id": rec["id"], "question": rec["question"], "tags": rec.get("tags") or [],
                    "exec_strict": rec.get("strict"), "exec_relaxed": rec.get("relaxed"),
                    "exec_diagnosis": rec.get("diagnosis"),
                    "llm_verdict": jr.verdict, "llm_reason": jr.reason, "llm_status": jr.status,
                    "agreement": agreement(rec.get("strict"), jr.verdict),
                    "gold": format_table(rec.get("gold_columns"), rec.get("gold_rows"), 5),
                    "pred": format_table(rec.get("pred_columns"), rec.get("pred_rows"), 5),
                    "pred_sql": rec.get("pred_sql"), "judge_model": judge_model,
                    "judge_raw": jr.raw, "judge_tokens": jr.tokens,
                }
                tag = ""
                log.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
                log.flush()
            rows.append(row)
            e = {True: "O", False: "X", None: "-"}[row["exec_strict"]]
            v = {1: "O", 0: "X", None: "?"}[row["llm_verdict"]]
            print(f"[{idx}/{len(records)}] 실행 {e} | LLM {v} {row['id']} {row['llm_status']} {tag}— {row['llm_reason']}")

    with log_path.open("w", encoding="utf-8") as log:
        for row in rows:
            log.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    return write_judge_outputs(rows, out_dir, judge_model)


def _stats(rows: list[dict]) -> dict:
    valid = [r for r in rows if r["exec_strict"] is not None]
    return {
        "n": len(valid),
        "exec_strict": sum(bool(r["exec_strict"]) for r in valid),
        "exec_relaxed": sum(bool(r["exec_relaxed"]) for r in valid),
        "llm": sum(r["llm_verdict"] == 1 for r in valid),
    }


def write_judge_outputs(rows: list[dict], out_dir: Path, judge_model: str) -> dict:
    cols = ["id", "question", "tags", "exec_strict", "exec_relaxed", "exec_diagnosis", "llm_verdict",
            "agreement", "llm_reason", "llm_status", "gold", "pred", "pred_sql"]
    with (out_dir / "judge_compare.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "tags": ",".join(r["tags"])})

    by_tag = defaultdict(list)
    for r in rows:
        for t in r["tags"] or ["(태그 없음)"]:
            by_tag[t].append(r)
    agree = defaultdict(int)
    for r in rows:
        agree[r["agreement"]] += 1
    summary = {
        "judge_model": judge_model,
        "overall": _stats(rows),
        "agreement": dict(agree),
        "judge_failed": [r["id"] for r in rows if r["llm_status"] in ("api_error", "parse_error")],
        "by_tag": {t: _stats(rs) for t, rs in sorted(by_tag.items())},
        "judge_tokens": sum(r.get("judge_tokens") or 0 for r in rows),
    }
    (out_dir / "judge_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "judge_summary.md").write_text(render_judge_summary(summary, rows), encoding="utf-8")
    return summary


def render_judge_summary(s: dict, rows: list[dict]) -> str:
    o, a = s["overall"], s["agreement"]
    lines = [
        f"# 실행 비교 vs LLM 채점 ({datetime.now():%Y-%m-%d %H:%M})", "",
        f"judge 모델: `{s['judge_model']}` / judge 토큰 합계: {s['judge_tokens']}", "",
        "| 기준 | 정답률 |", "|---|---|",
        f"| execution match (strict) | {_pct(o['exec_strict'], o['n'])} |",
        f"| execution match (relaxed) | {_pct(o['exec_relaxed'], o['n'])} |",
        f"| LLM-as-a-judge | {_pct(o['llm'], o['n'])} |", "",
        "## 두 기준의 일치 (strict 기준)", "",
        "| | LLM O | LLM X |", "|---|---|---|",
        f"| 실행 O | {a.get('both_correct', 0)} | {a.get('exec_only', 0)} |",
        f"| 실행 X | {a.get('llm_only', 0)} | {a.get('both_wrong', 0)} |", "",
    ]
    if s["judge_failed"]:
        lines += [f"> judge 판정 실패(오답으로 집계, 다시 실행하면 이 문항만 재시도): {', '.join(s['judge_failed'])}", ""]
    lines += ["## 유형별", "", "| 태그 | n | strict | relaxed | LLM |", "|---|---|---|---|---|"]
    for t, g in s["by_tag"].items():
        lines.append(f"| {t} | {g['n']} | {_pct(g['exec_strict'], g['n'])} | {_pct(g['exec_relaxed'], g['n'])} | {_pct(g['llm'], g['n'])} |")
    for kind in ("llm_only", "exec_only"):
        diff = [r for r in rows if r["agreement"] == kind]
        if not diff:
            continue
        lines += ["", f"## {AGREEMENT_DESC[kind]} ({len(diff)}개)", ""]
        for r in diff:
            lines += [f"### {r['id']} — 실행 진단 {r['exec_diagnosis']}", f"질문: {r['question']}", "",
                      f"- LLM 판정 이유: {r['llm_reason']}", "", "정답:", "```", r["gold"], "```",
                      "모델 답변:", "```", r["pred"], "```", ""]
    return "\n".join(lines) + "\n"


def make_judge_llm(settings: Settings | None = None):
    """평가용 ChatKHU 클라이언트. 같은 API, judge 모델·temperature 0 으로."""
    from .chatkhu_client import ChatKHUClient

    settings = settings or Settings()
    judge_settings = replace(settings, model=settings.judge_model or settings.model, temperature=0.0)
    return ChatKHUClient(judge_settings), judge_settings.model


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="results/ 아래 폴더 이름")
    ap.add_argument("--force", action="store_true", help="이전 판정을 무시하고 전부 다시 채점")
    args = ap.parse_args()

    llm, model = make_judge_llm()
    s = run_judge(RESULTS_DIR / args.run, llm, model, force=args.force)
    o = s["overall"]
    print(f"\nexecution strict {_pct(o['exec_strict'], o['n'])} | relaxed {_pct(o['exec_relaxed'], o['n'])}"
          f" | LLM judge {_pct(o['llm'], o['n'])} → {RESULTS_DIR / args.run / 'judge_summary.md'}")


if __name__ == "__main__":
    main()
