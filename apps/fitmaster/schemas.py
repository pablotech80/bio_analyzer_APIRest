from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field, conlist

from apps.ai_core.schemas import StrictModel


class FitMasterInput(StrictModel):
    inputs: Dict[str, Any]
    results: Dict[str, Any]
    interpretations: Dict[str, Any]
    goal: Optional[str] = None
    notes: Optional[str] = None
    history_summary: Optional[Dict[str, Any]] = None


class FitMasterOutputV1(StrictModel):
    interpretation: str
    nutrition_plan: Optional[Dict[str, Any]] = None
    training_plan: Optional[Dict[str, Any]] = None


class MacroBreakdown(StrictModel):
    protein_g: float
    carbs_g: float
    fat_g: float


class NutritionMeal(StrictModel):
    name: str = Field(max_length=80)
    foods: conlist(str, max_length=20) = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=400)


class NutritionPlan(StrictModel):
    daily_calories: Optional[int] = None
    macros: Optional[MacroBreakdown] = None
    meals: conlist(NutritionMeal, max_length=10) = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=800)


class TrainingSession(StrictModel):
    day: str = Field(max_length=24)
    focus: str = Field(max_length=80)
    exercises: conlist(str, max_length=20) = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=600)


class TrainingPlan(StrictModel):
    weekly_split: Dict[str, str] = Field(default_factory=dict)
    sessions: conlist(TrainingSession, max_length=10) = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=800)


class SafetyInfo(StrictModel):
    disclaimer: str = Field(max_length=600)
    contraindications: conlist(str, max_length=10) = Field(default_factory=list)


class FitMasterOutputV2(StrictModel):
    summary: str = Field(max_length=800)
    flags: conlist(str, max_length=20) = Field(default_factory=list)
    assumptions: conlist(str, max_length=20) = Field(default_factory=list)
    nutrition: NutritionPlan = Field(default_factory=NutritionPlan)
    training: TrainingPlan = Field(default_factory=TrainingPlan)
    next_steps: conlist(str, max_length=12) = Field(default_factory=list)
    safety: SafetyInfo = Field(
        default_factory=lambda: SafetyInfo(
            disclaimer="Consulte con un profesional de la salud antes de iniciar cambios.",
            contraindications=[],
        )
    )


# Alias maintained for existing imports pointing at the legacy schema.
FitMasterOutput = FitMasterOutputV1
