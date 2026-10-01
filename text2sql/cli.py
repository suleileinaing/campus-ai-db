"""단일 질문 실행 / 모델 목록 확인 / 프롬프트 미리보기.

  python -m text2sql.cli --list-models
  python -m text2sql.cli --show-prompt
  python -m text2sql.cli "2026년 2학기 월요일 13:30에 시작하는 수업 알려줘"
  python -m text2sql.cli --student-id 202210001 "내가 지금까지 이수한 학점은?"
  python -m text2sql.cli --student-id 202210001          # 대화형
"""

from __future__ import annotations

import argparse

from .config import Settings
from .executor import SQLExecutor
from .pipeline import Text2SQL
from .prompt import PromptBuilder


def print_output(out) -> None:
    for i, a in enumerate(out.attempts, 1):
        status = "OK" if a.ok else f"실패({a.error_kind}): {a.error}"
        print(f"\n[시도 {i}] {status}\n{a.sql}")
    res = out.result
    if res and res.ok:
        print("\n" + " | ".join(res.columns))
        for row in res.rows[:30]:
            print(" | ".join("" if v is None else str(v) for v in row))
        more = len(res.rows) - 30
        if more > 0 or res.truncated:
            print(f"... (+{max(more, 0)}행{', row_limit 도달' if res.truncated else ''})")
    print(f"\n토큰 {out.total_tokens}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--student-id", type=int, default=None)
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--show-prompt", action="store_true")
    ap.add_argument("--no-fewshot", action="store_true")
    args = ap.parse_args()

    settings = Settings()
    prompt = PromptBuilder(use_fewshot=not args.no_fewshot)
    if args.show_prompt:
        print(prompt.system_prompt())
        print(f"\n(약 {len(prompt.system_prompt())}자)")
        return

    from .chatkhu_client import ChatKHUClient
    llm = ChatKHUClient(settings)
    if args.list_models:
        print("\n".join(llm.list_models()))
        return

    engine = Text2SQL(llm, prompt, SQLExecutor(row_limit=settings.row_limit,
                      timeout_sec=settings.query_timeout_sec), settings.max_repair_attempts)
    if args.question:
        print_output(engine.ask(args.question, args.student_id))
        return
    while True:
        try:
            q = input("\n질문> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q in {"", "exit", "quit"}:
            break
        print_output(engine.ask(q, args.student_id))


if __name__ == "__main__":
    main()
