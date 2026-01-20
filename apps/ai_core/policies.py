from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PolicyDecision:
    blocked: bool
    reason: Optional[str] = None


class PolicyEngine:
    """Framework-agnostic policy evaluation. No Django imports allowed."""

    def evaluate(self, _request):
        return PolicyDecision(blocked=False)
