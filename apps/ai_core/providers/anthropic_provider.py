from __future__ import annotations

from .base import ProviderConfig, ProviderError


class AnthropicProvider:
    def __init__(self, _config: ProviderConfig) -> None:
        raise ProviderError("Anthropic provider not implemented in this repo yet")
