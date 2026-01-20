from __future__ import annotations

import os
from typing import Tuple

from apps.ai_core.providers import DummyProvider, OpenAIProvider, ProviderConfig, ProviderError


def get_provider_config() -> ProviderConfig:
    provider = os.getenv("AI_PROVIDER", "dummy").strip().lower()
    model_name = os.getenv("AI_MODEL_NAME", "gpt-4o-mini").strip()
    timeout_seconds = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    api_key = os.getenv("OPENAI_API_KEY") if provider == "openai" else None

    return ProviderConfig(
        provider=provider,
        model_name=model_name,
        timeout_seconds=timeout_seconds,
        api_key=api_key,
    )


def build_provider() -> Tuple[object, str]:
    cfg = get_provider_config()

    if cfg.provider == "dummy":
        return DummyProvider(message="ok"), cfg.model_name

    if cfg.provider == "openai":
        return OpenAIProvider(cfg), cfg.model_name

    raise ProviderError(f"Unsupported AI_PROVIDER: {cfg.provider}")
