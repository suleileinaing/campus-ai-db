"""질문 → SQL 생성 → 실행 → (오류 시) 자기수정 루프."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .answer import render_answer, split_answer_template
from .chatkhu_client import LLMClient
from .executor import ExecutionResult, SQLExecutor, extract_sql
import re

from .prompt import CLARIFY_TOKEN, REFUSE_TOKEN, PromptBuilder


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
    attempts: list[Attempt] = field(default_factory=list)
    answer: str | None = None  # 사용자에게 보여 줄 자연어 답변(값은 로컬에서 채움)

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
        self._system = prompt.system_prompt()

    def ask(self, question: str, student_id: int | None = None, history: list[dict] | None = None) -> Text2SQLOutput:
        """history: 앞선 턴의 user/assistant 메시지(다중턴). 결과 행은 넣지 않는다."""
        messages = [
            {"role": "system", "content": self._system},
            *(history or []),
            {"role": "user", "content": self.prompt.user_prompt(question, student_id)},
        ]
        out = Text2SQLOutput(question=question, student_id=student_id, final_sql=None, result=None)
        template = None

        for _ in range(self.max_repairs + 1):
            resp = self.llm.complete(messages)
            body, tmpl = split_answer_template(resp.text)
            template = tmpl or template  # 수정 응답에 틀이 없으면 앞 시도의 틀을 쓴다
            refused = re.search(rf"^\s*{REFUSE_TOKEN}\s*:?(.*)$", body, flags=re.M)
            clarify = None if refused else re.search(rf"^\s*{CLARIFY_TOKEN}\s*:?(.*)$", body, flags=re.M)
            sql = None if refused or clarify else extract_sql(body)
            if clarify:
                result = ExecutionResult(ok=False, error=f"모델이 되물음: {clarify.group(1).strip()}", error_kind="clarify")
            elif refused:
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
            if result.ok or result.error_kind in ("refused", "clarify"):
                break  # 모델이 스스로 거부하거나 되물은 경우는 다시 시도하지 않는다
            # 오류 메시지만 되돌려 준다(결과 행은 LLM 에 보내지 않음)
            messages.append({"role": "assistant", "content": resp.text})
            messages.append({"role": "user", "content": self.prompt.repair_prompt(sql or "(없음)", result.error or "")})
        out.answer = self._answer(out.result, template)
        return out

    @staticmethod
    def _answer(result: ExecutionResult | None, template: str | None) -> str:
        if result is None:
            return "죄송해요, 답을 만들지 못했어요."
        if result.ok:
            return render_answer(template, result.columns, result.rows)
        if result.error_kind == "clarify":
            return result.error.removeprefix("모델이 되물음:").strip()
        if result.error_kind in ("refused", "guard"):
            return "그 요청은 처리할 수 없어요. 본인 정보나 공개된 학사 정보만 조회할 수 있어요."
        return "죄송해요, 질문에 맞는 정보를 찾지 못했어요. 조금 더 구체적으로 물어봐 주세요."
