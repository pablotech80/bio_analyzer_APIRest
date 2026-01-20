from __future__ import annotations

from .base import ProviderConfig, ProviderError


class DeepSeekProvider:
    def __init__(self, _config: ProviderConfig) -> None:
        raise ProviderError("DeepSeek provider not implemented in this repo yet")
