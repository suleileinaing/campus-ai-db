"""gold 질의셋으로 Text2SQL 을 평가하고 results/<run_name>/ 에 결과를 저장한다.

사용 예:
  python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --run-name gpt_fewshot
  python -m text2sql.evaluate --gold ... --no-fewshot --run-name gpt_zeroshot
  python -m text2sql.evaluate --gold ... --oracle   # API 없이 파이프라인 점검(정답 SQL 을 그대로 예측으로 사용)
"""

from __future__ import annotations

import argparse
import re
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from .compare import compare_results, gold_is_ordered
from .config import RESULTS_DIR, Settings
from .executor import SQLExecutor
from .gold_loader import GoldItem, load_gold
from .pipeline import Text2SQL
from .prompt import PromptBuilder


def gold_warnings(item: GoldItem) -> list[str]:
    """정답 자체가 흔들릴 수 있는 문항을 표시한다(점수는 그대로 매기고 보고서에 따로 적는다)."""
    warns = []
    sql = re.sub(r"\s+", " ", (item.gold_sql or "")).upper()
    if " LIMIT " in f" {sql} " and not gold_is_ordered(item.gold_sql or ""):
        warns.append("LIMIT 이 있는데 ORDER BY 가 없어 정답 행이 실행마다 달라질 수 있음")
    return warns


def gold_rows_for(item: GoldItem, executor: SQLExecutor) -> tuple[list[tuple] | None, list[str], str | None]:
    """(정답 행, 정답 컬럼 이름, 오류)"""
    if item.expect_refusal:
        return None, [], None
    if item.gold_sql:
        res = executor.run(item.gold_sql, student_id=item.student_id, enforce_scope=False)
        if not res.ok:
            return None, [], f"gold SQL 실행 실패: {res.error}"
        if res.truncated:
            return None, [], "gold 결과가 row_limit 을 넘습니다. TEXT2SQL_ROW_LIMIT 을 늘리세요."
        return res.rows, res.columns, None
    rows = item.answer_rows()
    if rows is None:
        return None, [], "gold_sql 과 gold_answer 가 모두 비어 있습니다."
    return rows, [], None


def score_record(rec: dict, gold_rows, gold_columns, pred_rows, ordered: bool) -> None:
    """실행에 성공한 예측을 gold 와 비교해 rec 에 점수를 채운다. rescore 에서도 쓴다."""
    cmp = compare_results(gold_rows, pred_rows, ordered, gold_columns)
    rec.update(strict=cmp.strict, relaxed=cmp.relaxed, subset=cmp.subset, diagnosis=cmp.diagnosis,
               missing_columns=cmp.missing_columns, gold_row_count=cmp.gold_row_count,
               pred_row_count=cmp.pred_row_count)


def evaluate(items: list[GoldItem], engine: Text2SQL, executor: SQLExecutor, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for idx, item in enumerate(items, 1):
        gold_rows, gold_columns, gold_err = gold_rows_for(item, executor)
        ordered = item.ordered if item.ordered is not None else bool(item.gold_sql and gold_is_ordered(item.gold_sql))

        try:
            out = engine.ask(item.question, item.student_id)
            api_error = None
        except Exception as exc:  # API 오류(크레딧 부족, 네트워크 등)도 기록하고 계속 진행
            out, api_error = None, f"{type(exc).__name__}: {exc}"

        rec = {
            "id": item.id, "question": item.question, "student_id": item.student_id,
            "tags": item.tags, "gold_sql": item.gold_sql, "ordered": ordered,
            "gold_error": gold_err, "api_error": api_error,
            "expect_refusal": item.expect_refusal, "gold_warnings": gold_warnings(item), "note": item.note,
        }
        if out is not None:
            res = out.result
            rec.update({
                "pred_sql": out.final_sql,
                "n_attempts": len(out.attempts),
                "first_try_exec_ok": out.first_try_ok,
                "exec_ok": bool(res and res.ok),
                "exec_error": res.error if res and not res.ok else None,
                "exec_error_kind": res.error_kind if res and not res.ok else None,
                "total_tokens": out.total_tokens,
                "latency_sec": round(sum(a.latency_sec for a in out.attempts), 2),
                "pred_columns": res.columns if res else [],
                "pred_rows": [list(r) for r in res.rows] if res else [],
                "attempts": [a.__dict__ for a in out.attempts],
            })
        if gold_rows is not None:
            rec["gold_columns"] = gold_columns
            rec["gold_rows"] = [list(r) for r in gold_rows]

        if api_error:
            rec.update(strict=False, relaxed=False, subset=False, diagnosis="api_error")
        elif item.expect_refusal:
            kind = rec.get("exec_error_kind")
            if kind in ("refused", "guard"):
                rec.update(strict=True, relaxed=True, subset=True, diagnosis=f"correct_refusal:{kind}")
            elif rec.get("exec_ok") and not out.result.rows:
                # 거부는 안 했지만 아무것도 돌려주지 않음 → 유출은 없음
                rec.update(strict=False, relaxed=True, subset=True, diagnosis="no_leak_but_not_refused")
            else:
                rec.update(strict=False, relaxed=False, subset=False, diagnosis="should_have_refused")
        elif gold_err:
            rec.update(strict=None, relaxed=None, subset=None, diagnosis="gold_invalid")
        elif not rec.get("exec_ok"):
            rec.update(strict=False, relaxed=False, subset=False, diagnosis=f"exec_fail:{rec.get('exec_error_kind')}")
        else:
            score_record(rec, gold_rows, gold_columns, out.result.rows, ordered)
        records.append(rec)
        mark = "O" if rec["strict"] else ("△" if rec["relaxed"] else ("▽" if rec.get("subset") else "X"))
        extra = f" — {api_error}" if api_error else (f" (빠진 컬럼: {', '.join(rec['missing_columns'])})" if rec.get("missing_columns") else "")
        print(f"[{idx}/{len(items)}] {mark} {item.id} {rec['diagnosis']}{extra}")

    return write_outputs(records, out_dir)


def write_outputs(records: list[dict], out_dir: Path, suffix: str = "") -> dict:
    with (out_dir / f"results{suffix}.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

    csv_cols = ["id", "question", "student_id", "tags", "strict", "relaxed", "subset", "diagnosis", "missing_columns",
                "n_attempts", "first_try_exec_ok", "exec_error", "gold_sql", "pred_sql",
                "total_tokens", "latency_sec"]
    with (out_dir / f"results{suffix}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=csv_cols, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow({**r, "tags": ",".join(r["tags"]), "missing_columns": ",".join(r.get("missing_columns") or [])})

    summary = summarize(records)
    (out_dir / f"summary{suffix}.md").write_text(render_summary(summary, records), encoding="utf-8")
    (out_dir / f"summary{suffix}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def _pct(num: int, den: int) -> str:
    return f"{num}/{den} ({num / den:.1%})" if den else "0/0"


def _group_stats(recs: list[dict]) -> dict:
    valid = [r for r in recs if r["strict"] is not None]
    n = len(valid)
    return {
        "n": n,
        "exec_ok": sum(bool(r.get("exec_ok")) for r in valid),
        "first_try_exec_ok": sum(bool(r.get("first_try_exec_ok")) for r in valid),
        "strict": sum(bool(r["strict"]) for r in valid),
        "relaxed": sum(bool(r["relaxed"]) for r in valid),
        "subset": sum(bool(r.get("subset")) for r in valid),
    }


def summarize(records: list[dict]) -> dict:
    by_tag = defaultdict(list)
    for r in records:
        for t in r["tags"] or ["(태그 없음)"]:
            by_tag[t].append(r)
    toks = [r.get("total_tokens", 0) for r in records if r.get("total_tokens")]
    lats = [r.get("latency_sec", 0) for r in records if r.get("latency_sec")]
    return {
        "overall": _group_stats(records),
        "by_tag": {t: _group_stats(rs) for t, rs in sorted(by_tag.items())},
        "diagnosis": dict(Counter(r["diagnosis"] for r in records)),
        "gold_invalid": [r["id"] for r in records if r["diagnosis"] == "gold_invalid"],
        "avg_tokens": round(sum(toks) / len(toks), 1) if toks else 0,
        "avg_latency_sec": round(sum(lats) / len(lats), 2) if lats else 0,
    }


def render_summary(s: dict, records: list[dict]) -> str:
    o = s["overall"]
    lines = [
        f"# Text2SQL 평가 결과 ({datetime.now():%Y-%m-%d %H:%M})", "",
        "| 지표 | 값 |", "|---|---|",
        f"| 평가 문항 수 | {o['n']} |",
        f"| 실행 성공률(최종) | {_pct(o['exec_ok'], o['n'])} |",
        f"| 실행 성공률(1차 시도) | {_pct(o['first_try_exec_ok'], o['n'])} |",
        f"| 정답률 strict | {_pct(o['strict'], o['n'])} |",
        f"| 정답률 relaxed | {_pct(o['relaxed'], o['n'])} |",
        f"| 정답률 subset (정답 일부 컬럼 누락 허용) | {_pct(o['subset'], o['n'])} |",
        f"| 평균 토큰 | {s['avg_tokens']} |",
        f"| 평균 응답시간(초) | {s['avg_latency_sec']} |", "",
        "## 유형별", "", "| 태그 | n | strict | relaxed | subset | 실행 성공 |", "|---|---|---|---|---|---|",
    ]
    for t, g in s["by_tag"].items():
        lines.append(f"| {t} | {g['n']} | {_pct(g['strict'], g['n'])} | {_pct(g['relaxed'], g['n'])} | {_pct(g['subset'], g['n'])} | {_pct(g['exec_ok'], g['n'])} |")
    lines += ["", "## 진단 분포", "", "| 진단 | 개수 |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(s["diagnosis"].items(), key=lambda kv: -kv[1])]
    warned = [r for r in records if r.get("gold_warnings") or r.get("note")]
    if warned:
        lines += ["", "## 정답 재검토가 필요한 문항", ""]
        for r in warned:
            reasons = "; ".join([*r.get("gold_warnings", []), *([r["note"]] if r.get("note") else [])])
            lines.append(f"- {r['id']} ({'O' if r['strict'] else 'X'}): {r['question']} — {reasons}")
    if s["gold_invalid"]:
        lines += ["", f"> gold 자체가 실행되지 않아 제외된 문항: {', '.join(s['gold_invalid'])}"]
    fails = [r for r in records if r["strict"] is False]
    if fails:
        lines += ["", "## 오답 목록", ""]
        for r in fails:
            lines += [f"### {r['id']} — {r['diagnosis']}", f"질문: {r['question']}", "",
                      "gold:", "```sql", ("(거부가 정답)" if r.get("expect_refusal") else (r.get("gold_sql") or "(gold_answer 사용)")).strip(), "```",
                      "pred:", "```sql", (r.get("pred_sql") or "(없음)").strip(), "```"]
            if r.get("missing_columns"):
                lines.append(f"예측 값은 맞지만 빠진 정답 컬럼: {', '.join(r['missing_columns'])} → 핵심 정보인지 확인 필요")
            elif r.get("pred_columns") is not None and r.get("gold_columns"):
                lines.append(f"정답 컬럼: {', '.join(r['gold_columns'])} / 예측 컬럼: {', '.join(r.get('pred_columns') or [])}")
                lines.append(f"정답 행 수: {r.get('gold_row_count')} / 예측 행 수: {r.get('pred_row_count')}")
            if r.get("exec_error"):
                lines.append(f"오류: {r['exec_error']}")
            lines.append("")
    lines += ["", "## 진단 코드 설명", "",
              "- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)",
              "- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)",
              "- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름",
              "- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패",
              "- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부",
              "- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행",
              "- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제"]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True, help="gold 질의셋(.json/.csv)")
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--no-fewshot", action="store_true")
    ap.add_argument("--max-fewshot", type=int, default=None)
    ap.add_argument("--limit", type=int, default=None, help="앞에서부터 N개만(크레딧 절약용)")
    ap.add_argument("--oracle", action="store_true", help="API 없이 gold SQL 을 예측으로 사용해 파이프라인 점검")
    args = ap.parse_args()

    settings = Settings()
    items = load_gold(args.gold)[: args.limit]
    executor = SQLExecutor(row_limit=settings.row_limit, timeout_sec=settings.query_timeout_sec)
    prompt = PromptBuilder(
        use_fewshot=not args.no_fewshot,
        exclude_sqls=[i.gold_sql for i in items if i.gold_sql],
        max_fewshot=args.max_fewshot,
    )
    if args.oracle:
        from .tests.mock_llm import OracleLLM
        llm = OracleLLM({i.question: (None if i.expect_refusal else (i.gold_sql or "SELECT 1")) for i in items})
        model_name = "oracle"
    else:
        from .chatkhu_client import ChatKHUClient
        llm = ChatKHUClient(settings)
        model_name = settings.model

    run_name = args.run_name or f"{model_name}_{'zeroshot' if args.no_fewshot else 'fewshot'}_{time.strftime('%m%d_%H%M')}"
    out_dir = RESULTS_DIR / run_name.replace("/", "_")
    engine = Text2SQL(llm, prompt, executor, max_repairs=settings.max_repair_attempts)
    (out_dir).mkdir(parents=True, exist_ok=True)
    (out_dir / "system_prompt.txt").write_text(prompt.system_prompt(), encoding="utf-8")
    (out_dir / "config.json").write_text(json.dumps({
        "model": model_name, "fewshot": not args.no_fewshot, "n_fewshot": len(prompt.fewshot),
        "temperature": settings.temperature, "max_repairs": settings.max_repair_attempts,
        "gold": str(args.gold), "n_items": len(items),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    s = evaluate(items, engine, executor, out_dir)
    o = s["overall"]
    print(f"\nstrict {_pct(o['strict'], o['n'])} | relaxed {_pct(o['relaxed'], o['n'])} | subset {_pct(o['subset'], o['n'])} → {out_dir}")


if __name__ == "__main__":
    main()