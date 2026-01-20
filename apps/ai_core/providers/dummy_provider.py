from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from apps.ai_core.runner import LLMResult


@dataclass
class DummyProvider:
    """Deterministic provider for local smoke tests (no network)."""

    message: str = "ok"

    def complete(self, *, model: str, system: str, user: str, max_tokens: Optional[int] = None) -> LLMResult:
        return LLMResult(
            text=json.dumps(
                {
                    "interpretation": self.message,
                    "nutrition_plan": None,
                    "training_plan": None,
                }
            ),
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            estimated_cost_usd=0.0,
        )
