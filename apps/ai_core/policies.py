from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


class PolicyViolation(Exception):
    """Raised when a policy blocks execution."""


@dataclass(frozen=True)
class BudgetPolicy:
    """
    Budget guardrails. Keep it simple for MVP:
    - max_input_chars: protects from massive user text
    - max_output_chars: protects from runaway completions (proxy for tokens)
    - max_tokens: optional if your provider returns token counts
    """

    max_input_chars: int = 8_000
    max_output_chars: int = 20_000
    max_tokens: Optional[int] = None


class InjectionDetector:
    """
    Basic prompt-injection / jailbreak detector.
    Not perfect, but good enough as L2 MVP gate.
    """

    _PATTERNS = [
        r"\bignore (all|any) (previous|prior) instructions\b",
        r"\byou are now\b",
        r"\bdeveloper mode\b",
        r"\bshow (me )?(your|the) (system prompt|prompt)\b",
        r"\breveal (secrets|keys|credentials)\b",
        r"\bexfiltrate\b",
        r"\bprompt injection\b",
        r"\bjailbreak\b",
        r"\bDAN\b",
    ]

    def __init__(self) -> None:
        self._regexes = [re.compile(p, re.IGNORECASE) for p in self._PATTERNS]

    def detect(self, text: str) -> bool:
        if not text:
            return False
        return any(rx.search(text) for rx in self._regexes)


def enforce_budget_input(text: str, budget: BudgetPolicy) -> None:
    if text and len(text) > budget.max_input_chars:
        raise PolicyViolation(f"input_too_large: {len(text)} > {budget.max_input_chars}")


def enforce_budget_output(raw: str, budget: BudgetPolicy) -> None:
    if raw and len(raw) > budget.max_output_chars:
        raise PolicyViolation(f"output_too_large: {len(raw)} > {budget.max_output_chars}")
