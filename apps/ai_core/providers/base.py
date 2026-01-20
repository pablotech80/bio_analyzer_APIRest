from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class ProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    model_name: str
    timeout_seconds: float = 30.0
    api_key: Optional[str] = None
