from __future__ import annotations

from .base import ProviderConfig, ProviderError


class GoogleProvider:
    def __init__(self, _config: ProviderConfig) -> None:
        raise ProviderError("Google provider not implemented in this repo yet")
