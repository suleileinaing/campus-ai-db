"""다중턴 대화 질의셋으로 Text2SQL 을 평가한다.

대화마다 앞 턴의 질문과 모델이 실제로 낸 응답을 다음 턴 메시지에 쌓는다(정답은 채점에만 쓴다).
조회 결과 행은 단일턴과 마찬가지로 LLM 에 보내지 않는다.

  python -m text2sql.evaluate_multiturn --gold text2sql/gold/다중턴_12대화_36턴.json --no-fewshot --model gemini-4-argon
  python -m text2sql.evaluate_multiturn --gold ... --oracle   # API 없이 점검(정답 SQL 을 예측으로 사용)
"""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from dataclasses import replace

from .config import RESULTS_DIR, Settings
from .evaluate import _pct, score_record, write_outputs
from .executor import SQLExecutor
from .gold_loader import GoldItem
from .pipeline import Text2SQL
from .prompt import CLARIFY_TOKEN, PromptBuilder


def load_dialogues(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def turn_item(conv: dict, turn: dict) -> GoldItem:
    return GoldItem(
        id=f"{conv['conversation_id']}-T{turn['turn']}", question=turn["user"],
        gold_answer=None if turn["expected_action"] == "clarify" else turn["gold_answer"],
        ordered=turn.get("ordered", False),
        tags=[conv["task_type"], f"turn{turn['turn']}", turn["expected_action"]],
        note=turn.get("self_contained_question", ""), reference_sql=turn.get("reference_sql"),
    )


def score_turn(rec: dict, item: GoldItem, expected: str, out) -> None:
    kind = rec.get("exec_error_kind")
    if rec.get("api_error"):
        rec.update(strict=False, relaxed=False, subset=False, diagnosis="api_error")
    elif expected == "clarify":
        ok = kind == "clarify"
        rec.update(strict=ok, relaxed=ok, subset=ok, diagnosis="correct_clarify" if ok else "should_have_clarified")
    elif not rec.get("exec_ok"):
        rec.update(strict=False, relaxed=False, subset=False, diagnosis=f"exec_fail:{kind}")
    else:
        rec["gold_columns"] = item.answer_columns()
        rec["gold_rows"] = [list(r) for r in item.answer_rows()]
        score_record(rec, item.answer_rows(), item.answer_columns(), out.result.rows, bool(item.ordered))


def run_dialogues(dialogues: list[dict], engine: Text2SQL, prompt: PromptBuilder) -> list[dict]:
    records = []
    for conv in dialogues:
        history: list[dict] = []
        for turn in conv["turns"]:
            item = turn_item(conv, turn)
            try:
                out, api_error = engine.ask(item.question, None, history), None
            except Exception as exc:  # API 오류도 기록하고 계속 진행
                out, api_error = None, f"{type(exc).__name__}: {exc}"

            rec = {"id": item.id, "conversation_id": conv["conversation_id"], "turn": turn["turn"],
                   "question": item.question, "student_id": None, "tags": item.tags,
                   "expected_action": turn["expected_action"], "gold_sql": None, "reference_sql": item.reference_sql,
                   "api_error": api_error, "note": item.note, "n_history_msgs": len(history)}
            if out is not None:
                res = out.result
                rec.update({
                    "pred_sql": out.final_sql, "n_attempts": len(out.attempts),
                    "first_try_exec_ok": out.first_try_ok, "exec_ok": bool(res and res.ok),
                    "exec_error": res.error if res and not res.ok else None,
                    "exec_error_kind": res.error_kind if res and not res.ok else None,
                    "total_tokens": out.total_tokens,
                    "latency_sec": round(sum(a.latency_sec for a in out.attempts), 2),
                    "pred_columns": res.columns if res else [],
                    "pred_rows": [list(r) for r in res.rows] if res else [],
                    "attempts": [a.__dict__ for a in out.attempts],
                })
            score_turn(rec, item, turn["expected_action"], out)
            records.append(rec)
            mark = "O" if rec["strict"] else ("△" if rec["relaxed"] else ("▽" if rec.get("subset") else "X"))
            print(f"[{len(records)}] {mark} {item.id} {rec['diagnosis']}" + (f" — {api_error}" if api_error else ""))

            # 다음 턴에는 이번 질문과 모델의 최종 응답만 넘긴다(결과 행은 보내지 않음)
            history.append({"role": "user", "content": prompt.user_prompt(item.question, None)})
            reply = out.attempts[-1].raw_response if out and out.attempts else "(응답 없음)"
            history.append({"role": "assistant", "content": reply})
    return records


def conversation_summary(records: list[dict]) -> dict:
    by_conv = defaultdict(list)
    for r in records:
        by_conv[r["conversation_id"]].append(r)
    by_turn = defaultdict(list)
    for r in records:
        by_turn[r["turn"]].append(r)
    return {
        "conversations": len(by_conv),
        "all_turns_strict": sum(all(r["strict"] for r in rs) for rs in by_conv.values()),
        "all_turns_relaxed": sum(all(r["relaxed"] for r in rs) for rs in by_conv.values()),
        "by_turn": {t: {"n": len(rs), "strict": sum(bool(r["strict"]) for r in rs),
                        "relaxed": sum(bool(r["relaxed"]) for r in rs)} for t, rs in sorted(by_turn.items())},
        "per_conversation": {c: "".join("O" if r["strict"] else "△" if r["relaxed"] else "X" for r in rs)
                             for c, rs in by_conv.items()},
    }


def render_conversation_summary(c: dict) -> str:
    lines = ["# 다중턴 요약", "",
             f"- 모든 턴 정답인 대화: strict {_pct(c['all_turns_strict'], c['conversations'])}"
             f" / relaxed {_pct(c['all_turns_relaxed'], c['conversations'])}", "",
             "| 턴 | n | strict | relaxed |", "|---|---|---|---|"]
    lines += [f"| {t} | {g['n']} | {_pct(g['strict'], g['n'])} | {_pct(g['relaxed'], g['n'])} |" for t, g in c["by_turn"].items()]
    lines += ["", "| 대화 | 턴별 결과 (O strict, △ relaxed, X 오답) |", "|---|---|"]
    lines += [f"| {cid} | {marks} |" for cid, marks in c["per_conversation"].items()]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True, help="다중턴 대화 질의셋(.json)")
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--no-fewshot", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="앞에서부터 N개 대화만(크레딧 절약용)")
    ap.add_argument("--oracle", action="store_true", help="API 없이 reference_sql 을 예측으로 사용해 점검")
    ap.add_argument("--model", default=None, help=".env 의 CHATKHU_MODEL 대신 쓸 생성 모델")
    args = ap.parse_args()

    settings = Settings()
    if args.model:
        settings = replace(settings, model=args.model)
    dialogues = load_dialogues(args.gold)[: args.limit]
    turns = [t for c in dialogues for t in c["turns"]]
    executor = SQLExecutor(row_limit=settings.row_limit, timeout_sec=settings.query_timeout_sec)
    prompt = PromptBuilder(use_fewshot=not args.no_fewshot, multiturn=True,
                           exclude_sqls=[t["reference_sql"] for t in turns if t.get("reference_sql")])
    if args.oracle:
        # 같은 문장의 후속 질문이 여러 대화에 있어서 질문 → SQL 매핑 대신 턴 순서대로 정답을 돌려준다
        from .tests.mock_llm import ScriptedLLM
        llm = ScriptedLLM([f"{CLARIFY_TOKEN}: 분반을 알려주세요." if t["expected_action"] == "clarify"
                           else f"```sql\n{t['reference_sql']}\n```" for t in turns])
        model_name = "oracle"
    else:
        from .chatkhu_client import ChatKHUClient
        llm = ChatKHUClient(settings)
        model_name = settings.model

    run_name = args.run_name or f"multiturn_{model_name}_{'zeroshot' if args.no_fewshot else 'fewshot'}_{time.strftime('%m%d_%H%M')}"
    out_dir = RESULTS_DIR / run_name.replace("/", "_")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "system_prompt.txt").write_text(prompt.system_prompt(), encoding="utf-8")
    (out_dir / "config.json").write_text(json.dumps({
        "model": model_name, "fewshot": not args.no_fewshot, "n_fewshot": len(prompt.fewshot),
        "temperature": settings.temperature, "max_repairs": settings.max_repair_attempts,
        "gold": str(args.gold), "n_conversations": len(dialogues), "n_turns": len(turns),
        "history": "앞 턴의 질문 + 모델의 실제 최종 응답(결과 행 제외)",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    engine = Text2SQL(llm, prompt, executor, max_repairs=settings.max_repair_attempts)
    records = run_dialogues(dialogues, engine, prompt)
    s = write_outputs(records, out_dir)["overall"]
    c = conversation_summary(records)
    (out_dir / "multiturn_summary.md").write_text(render_conversation_summary(c), encoding="utf-8")
    (out_dir / "multiturn_summary.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n턴 기준 strict {_pct(s['strict'], s['n'])} | relaxed {_pct(s['relaxed'], s['n'])} | subset {_pct(s['subset'], s['n'])}"
          f"\n모든 턴 정답인 대화 strict {_pct(c['all_turns_strict'], c['conversations'])}"
          f" | relaxed {_pct(c['all_turns_relaxed'], c['conversations'])} → {out_dir}")


if __name__ == "__main__":
    main()
