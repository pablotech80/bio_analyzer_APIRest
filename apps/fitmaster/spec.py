from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Type

from apps.ai_core.policies import BudgetPolicy, InjectionDetector
from apps.ai_core.runner import AgentSpec
from apps.ai_core.schemas import StrictModel, schema_json

from .prompts import SYSTEM_PROMPT
from .schemas import (
    FitMasterInput,
    FitMasterOutputV1,
    FitMasterOutputV2,
    NutritionPlan,
    SafetyInfo,
    TrainingPlan,
)


@dataclass(frozen=True)
class FitMasterSpec:
    name: str = "fitmaster"
    version: str = "0.1"


def _resolve_output_model(version: str) -> Type[StrictModel]:
    version = version.lower()
    if version == "v1":
        return FitMasterOutputV1
    return FitMasterOutputV2


def build_fitmaster_spec(
    *, model_name: str = "dummy", output_version: Optional[str] = None
) -> AgentSpec:
    selected_version = (output_version or os.getenv("FITMASTER_OUTPUT_VERSION", "v2")).lower()
    output_model = _resolve_output_model(selected_version)
    schema = schema_json(output_model)

    def build_system_prompt() -> str:
        return SYSTEM_PROMPT

    def build_user_prompt(input_obj: FitMasterInput) -> str:
        return (
            "Return ONLY valid JSON matching the required schema (no markdown).\n\n"
            f"Schema:\n{schema}\n\n"
            "Use the provided biometrics (inputs/results/interpretations) to populate the schema.\n\n"
            f"Data:\n{input_obj.model_dump_json(exclude_none=True)}"
        )

    def fallback_output(reason: str):
        if output_model is FitMasterOutputV1:
            return FitMasterOutputV1(
                interpretation=f"No se pudo generar el análisis FitMaster. ({reason})",
                nutrition_plan=None,
                training_plan=None,
            )
        return FitMasterOutputV2(
            summary=f"No se pudo generar el análisis FitMaster. ({reason})",
            flags=["fallback"],
            assumptions=[],
            nutrition=NutritionPlan(notes="Sin recomendaciones disponibles."),
            training=TrainingPlan(notes="Sin recomendaciones disponibles."),
            next_steps=["Intenta nuevamente más tarde."],
            safety=SafetyInfo(
                disclaimer="Consulta con un profesional de la salud antes de actuar.",
                contraindications=[],
            ),
        )

    return AgentSpec(
        name="fitmaster",
        version="0.1",
        model_name=model_name,
        input_model=FitMasterInput,
        output_model=output_model,
        budget=BudgetPolicy(),
        injection_detector=InjectionDetector(),
        build_system_prompt=build_system_prompt,
        build_user_prompt=build_user_prompt,
        fallback_output=fallback_output,
    )
