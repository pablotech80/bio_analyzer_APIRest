from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import Field

from apps.ai_core.schemas import StrictModel


class FitMasterInput(StrictModel):
    inputs: Dict[str, Any]
    results: Dict[str, Any]
    interpretations: Dict[str, Any]
    goal: Optional[str] = None
    notes: Optional[str] = None
    history_summary: Optional[Dict[str, Any]] = None


class FitMasterOutput(StrictModel):
    interpretation: str
    nutrition_plan: Optional[Dict[str, Any]] = None
    training_plan: Optional[Dict[str, Any]] = None
