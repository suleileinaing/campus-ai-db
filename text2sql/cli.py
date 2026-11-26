"""단일 질문 실행 / 모델 목록 확인 / 프롬프트 미리보기.

  python -m text2sql.cli --list-models
  python -m text2sql.cli --show-prompt
  python -m text2sql.cli "2026년 2학기 월요일 13:30에 시작하는 수업 알려줘"
  python -m text2sql.cli --student-id 202210001 "내가 지금까지 이수한 학점은?"
  python -m text2sql.cli --student-id 202210001          # 대화형(앞 대화를 기억, 'reset' 으로 초기화)
  python -m text2sql.cli --debug "..."                   # 자연어 답변과 함께 SQL·결과 표도 출력
  python -m text2sql.cli "캡스톤디자인 팀플이야?"          # 강의계획서 본문 질문은 검색(RAG)으로 답함
  python -m text2sql.cli --no-rag "..."                  # 본문 검색 끄기(rag_index 가 없으면 자동으로 꺼짐)
"""

from __future__ import annotations

import argparse
from dataclasses import replace

from .config import Settings
from .executor import SQLExecutor
from .pipeline import Text2SQL
from .prompt import PromptBuilder


def print_output(out, debug: bool = False) -> None:
    print(f"\n{out.answer}")
    if out.route == "search" and out.sources:
        print(f"(근거: {', '.join(out.sources)} 강의계획서)")
    if not debug:
        return
    print(f"\n[경로] {out.route}")
    for i, a in enumerate(out.attempts, 1):
        if a.error_kind == "search":  # SQL 대신 본문 검색으로 보낸 경우
            print(f"\n[시도 {i}] {a.error}")
            continue
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
    ap.add_argument("--model", default=None, help=".env 의 CHATKHU_MODEL 대신 쓸 모델")
    ap.add_argument("--debug", action="store_true", help="SQL·시도 기록·결과 표도 출력")
    ap.add_argument("--no-rag", action="store_true", help="강의계획서 본문 검색(RAG) 끄기")
    args = ap.parse_args()

    settings = Settings()
    if args.model:
        settings = replace(settings, model=args.model)
    interactive = not args.question
    from .syllabus_rag import SyllabusRetriever
    use_rag = not args.no_rag and SyllabusRetriever.exists()
    prompt = PromptBuilder(use_fewshot=not args.no_fewshot, multiturn=interactive, answer_template=True,
                           search=use_rag)
    if args.show_prompt:
        print(prompt.system_prompt())
        print(f"\n(약 {len(prompt.system_prompt())}자)")
        return

    from .chatkhu_client import ChatKHUClient
    llm = ChatKHUClient(settings)
    if args.list_models:
        print("\n".join(llm.list_models()))
        return

    retriever = SyllabusRetriever(llm=llm, embed_client=llm.client) if use_rag else None
    engine = Text2SQL(llm, prompt, SQLExecutor(row_limit=settings.row_limit,
                      timeout_sec=settings.query_timeout_sec), settings.max_repair_attempts, retriever=retriever)
    if args.question:
        print_output(engine.ask(args.question, args.student_id), args.debug)
        return
    history: list[dict] = []  # 앞 턴의 질문과 모델 응답(결과 행은 넣지 않음)
    while True:
        try:
            q = input("\n질문> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q in {"", "exit", "quit"}:
            break
        if q == "reset":
            history.clear()
            print("대화를 처음부터 시작해요.")
            continue
        out = engine.ask(q, args.student_id, history)
        print_output(out, args.debug)
        history.append({"role": "user", "content": prompt.user_prompt(q, args.student_id)})
        history.append({"role": "assistant", "content": out.attempts[-1].raw_response if out.attempts else ""})


if __name__ == "__main__":
    main()
