"""ChatKHU API Gateway(OpenAI 호환 Chat Completions) 클라이언트."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol

from .config import Settings


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_sec: float = 0.0
    raw: dict = field(default_factory=dict)


class LLMClient(Protocol):
    def complete(self, messages: list[dict]) -> LLMResponse: ...


class ChatKHUClient:
    def __init__(self, settings: Settings | None = None, max_retries: int = 3):
        from openai import OpenAI  # pip install openai

        self.settings = settings or Settings()
        if not self.settings.api_key:
            raise RuntimeError("CHATKHU_API_KEY 가 없습니다. text2sql/.env 를 확인하세요.")
        self.client = OpenAI(
            api_key=self.settings.api_key,
            base_url=self.settings.base_url,
            timeout=self.settings.request_timeout_sec,
            max_retries=max_retries,
        )

    def list_models(self) -> list[str]:
        return sorted(m.id for m in self.client.models.list())

    def complete(self, messages: list[dict]) -> LLMResponse:
        if not self.settings.model:
            raise RuntimeError("CHATKHU_MODEL 이 비어 있습니다. --list-models 로 확인 후 .env 에 넣으세요.")
        kwargs: dict = {"model": self.settings.model, "messages": messages}
        if self.settings.temperature is not None:
            kwargs["temperature"] = self.settings.temperature

        start = time.perf_counter()
        try:
            resp = self.client.chat.completions.create(**kwargs)
        except Exception as exc:  # temperature 미지원 모델이면 빼고 한 번 더 시도
            if "temperature" in kwargs and "temperature" in str(exc).lower():
                kwargs.pop("temperature")
                resp = self.client.chat.completions.create(**kwargs)
            else:
                raise
        latency = time.perf_counter() - start

        usage = getattr(resp, "usage", None)
        return LLMResponse(
            text=resp.choices[0].message.content or "",
            model=getattr(resp, "model", self.settings.model),
            prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
            completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
            latency_sec=latency,
        )
