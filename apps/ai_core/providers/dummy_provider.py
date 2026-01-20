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
        response = {
            "summary": self.message,
            "flags": [],
            "assumptions": [],
            "nutrition": {
                "daily_calories": 2200,
                "macros": {"protein_g": 150, "carbs_g": 220, "fat_g": 70},
                "meals": [],
                "notes": None,
            },
            "training": {
                "weekly_split": {"day_1": "full_body"},
                "sessions": [],
                "notes": None,
            },
            "next_steps": ["Mantén consistencia durante 4 semanas."],
            "safety": {
                "disclaimer": "Consulta con un profesional de la salud antes de actuar.",
                "contraindications": [],
            },
        }
        return LLMResult(
            text=json.dumps(response),
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            estimated_cost_usd=0.0,
        )
