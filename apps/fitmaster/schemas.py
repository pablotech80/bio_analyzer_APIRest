from __future__ import annotations

from typing import Optional

from pydantic import Field

from apps.ai_core.schemas import StrictModel


class FitMasterInput(StrictModel):
    age: int = Field(..., ge=0, le=120)
    height_cm: float = Field(..., gt=0, le=250)
    weight_kg: float = Field(..., gt=0, le=500)
    goal: Optional[str] = None
    notes: Optional[str] = None


class FitMasterOutput(StrictModel):
    message: str
