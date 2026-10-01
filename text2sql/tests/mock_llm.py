"""API 없이 파이프라인을 점검하기 위한 가짜 LLM."""

from __future__ import annotations

import re

from ..chatkhu_client import LLMResponse


def _last_question(messages: list[dict]) -> str:
    for m in messages:
        if m["role"] == "user" and "질문:" in m["content"]:
            return m["content"].split("질문:", 1)[1].strip()
    return ""


class OracleLLM:
    """질문 → 정답 SQL 을 그대로 돌려준다(평가 코드가 100% 나와야 정상)."""

    def __init__(self, answers: dict[str, str | None]):
        self.answers = answers

    def complete(self, messages: list[dict]) -> LLMResponse:
        q = _last_question(messages)
        sql = self.answers.get(q)
        if q in self.answers and sql is None:  # 거부가 정답인 문항
            return LLMResponse(text="REFUSE: 다른 학생 정보", model="oracle")
        return LLMResponse(text=f"```sql\n{sql or 'SELECT 1'}\n```", model="oracle")


class BrokenThenFixedLLM:
    """첫 응답은 틀린 컬럼명, 수정 요청을 받으면 정답을 준다(자기수정 루프 점검)."""

    def __init__(self, answers: dict[str, str]):
        self.answers = answers

    def complete(self, messages: list[dict]) -> LLMResponse:
        sql = self.answers[_last_question(messages)]
        if len(messages) == 2:
            sql = re.sub(r"\bcourse_name\b", "course_title", sql, count=1)
        return LLMResponse(text=f"설명입니다.\n```sql\n{sql}\n```", model="mock", prompt_tokens=10, completion_tokens=5)


class ScriptedLLM:
    """정해진 응답을 순서대로 돌려준다."""

    def __init__(self, replies: list[str]):
        self.replies = list(replies)

    def complete(self, messages: list[dict]) -> LLMResponse:
        return LLMResponse(text=self.replies.pop(0), model="scripted")
