"""질문 → SQL 생성 → 실행 → (오류 시) 자기수정 루프."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .chatkhu_client import LLMClient
from .executor import ExecutionResult, SQLExecutor, extract_sql
import re

from .prompt import REFUSE_TOKEN, PromptBuilder


@dataclass
class Attempt:
    raw_response: str
    sql: str | None
    ok: bool
    error: str | None
    error_kind: str | None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_sec: float = 0.0


@dataclass
class Text2SQLOutput:
    question: str
    student_id: int | None
    final_sql: str | None
    result: ExecutionResult | None
    fewshot_titles: list[str] = field(default_factory=list)
    attempts: list[Attempt] = field(default_factory=list)
    bilingual_text_search_used: bool = False
    bilingual_text_search_retry_used: bool = False

    @property
    def first_try_ok(self) -> bool:
        return bool(self.attempts) and self.attempts[0].ok

    @property
    def total_tokens(self) -> int:
        return sum(a.prompt_tokens + a.completion_tokens for a in self.attempts)

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.result is not None:
            d["result"] = {
                "ok": self.result.ok, "columns": self.result.columns,
                "rows": [list(r) for r in self.result.rows], "error": self.result.error,
                "truncated": self.result.truncated,
            }
        return d


class Text2SQL:
    def __init__(self, llm: LLMClient, prompt: PromptBuilder, executor: SQLExecutor, max_repairs: int = 2):
        self.llm = llm
        self.prompt = prompt
        self.executor = executor
        self.max_repairs = max_repairs

    def ask(self, question: str, student_id: int | None = None) -> Text2SQLOutput:
        selected_fewshot = self.prompt.fewshot_for(question)
        base_system_prompt = self.prompt.system_prompt(question)
        initial_system_prompt = base_system_prompt
        bilingual_text_search_used = False
        if self.prompt.bilingual_text_search:
            targeted_system_prompt = self.prompt.system_prompt(
                question,
                include_bilingual_text=True,
            )
            if targeted_system_prompt != base_system_prompt:
                initial_system_prompt = targeted_system_prompt
                bilingual_text_search_used = True
        messages = [
            {"role": "system", "content": initial_system_prompt},
            {"role": "user", "content": self.prompt.user_prompt(question, student_id)},
        ]
        out = Text2SQLOutput(
            question=question,
            student_id=student_id,
            final_sql=None,
            result=None,
            fewshot_titles=[e.title for e in selected_fewshot],
            bilingual_text_search_used=bilingual_text_search_used,
        )

        repair_count = 0
        bilingual_retry_done = False
        while True:
            resp = self.llm.complete(messages)
            refused = re.search(rf"^\s*{REFUSE_TOKEN}\s*:?(.*)$", resp.text, flags=re.M)
            sql = None if refused else extract_sql(resp.text)
            if refused:
                reason = refused.group(1).strip() or "거부"
                result = ExecutionResult(ok=False, error=f"모델이 거부함: {reason}", error_kind="refused")
            elif sql is None:
                result = ExecutionResult(ok=False, error="응답에서 SQL 을 찾지 못했습니다.", error_kind="no_sql")
            else:
                result = self.executor.run(sql, student_id=student_id)

            out.attempts.append(Attempt(
                raw_response=resp.text, sql=sql, ok=result.ok, error=result.error,
                error_kind=result.error_kind, prompt_tokens=resp.prompt_tokens,
                completion_tokens=resp.completion_tokens, latency_sec=resp.latency_sec,
            ))
            out.final_sql, out.result = sql, result
            if result.ok:
                no_usable_values = not result.rows or all(
                    value is None for row in result.rows for value in row
                )
                if (self.prompt.bilingual_text_search and not bilingual_text_search_used
                        and not bilingual_retry_done and no_usable_values):
                    grounded_system_prompt = self.prompt.system_prompt(
                        question,
                        include_bilingual_text=True,
                        force_bilingual_text=True,
                    )
                    if grounded_system_prompt != base_system_prompt:
                        messages = [
                            {"role": "system", "content": grounded_system_prompt},
                            {"role": "user", "content": self.prompt.user_prompt(question, student_id)},
                        ]
                        bilingual_retry_done = True
                        out.bilingual_text_search_retry_used = True
                        continue
                break
            if result.error_kind == "refused":
                break  # 모델이 스스로 거부한 경우는 다시 시도하지 않는다
            if repair_count >= self.max_repairs:
                break
            repair_count += 1
            # 오류 메시지만 되돌려 준다(결과 행은 LLM 에 보내지 않음)
            messages.append({"role": "assistant", "content": resp.text})
            messages.append({"role": "user", "content": self.prompt.repair_prompt(sql or "(없음)", result.error or "")})
        return out
