from __future__ import annotations

from typing import Optional

from openai import OpenAI

from apps.ai_core.runner import LLMResult

from .base import ProviderConfig, ProviderError


class OpenAIProvider:
    def __init__(self, config: ProviderConfig) -> None:
        if not config.api_key:
            raise ProviderError("OPENAI_API_KEY is required for OpenAIProvider")

        # OpenAI SDK supports timeout at client init (best-effort).
        self._client = OpenAI(api_key=config.api_key, timeout=config.timeout_seconds)

    def complete(self, *, model: str, system: str, user: str, max_tokens: Optional[int] = None) -> LLMResult:
        resp = self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )

        text = resp.choices[0].message.content or ""
        usage = getattr(resp, "usage", None)

        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None
        total_tokens = getattr(usage, "total_tokens", None) if usage else None

        return LLMResult(
            text=text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=None,
        )
