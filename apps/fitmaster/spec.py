from __future__ import annotations

from dataclasses import dataclass

from apps.ai_core.policies import BudgetPolicy, InjectionDetector
from apps.ai_core.runner import AgentSpec

from .prompts import SYSTEM_PROMPT
from .schemas import FitMasterInput, FitMasterOutput


@dataclass(frozen=True)
class FitMasterSpec:
    name: str = "fitmaster"
    version: str = "0.1"


def build_fitmaster_spec(*, model_name: str = "dummy") -> AgentSpec:
    def build_system_prompt() -> str:
        return SYSTEM_PROMPT

    def build_user_prompt(input_obj: FitMasterInput) -> str:
        # Keep prompt minimal for scaffold. Actual prompt will be refined later.
        return (
            "Return ONLY valid JSON with keys exactly matching the schema. "
            "Do not include markdown.\n\n"
            f"Input:\n{input_obj.model_dump_json(exclude_none=True)}"
        )

    def fallback_output(reason: str) -> FitMasterOutput:
        return FitMasterOutput(message=f"FitMaster fallback ({reason})")

    return AgentSpec(
        name="fitmaster",
        version="0.1",
        model_name=model_name,
        input_model=FitMasterInput,
        output_model=FitMasterOutput,
        budget=BudgetPolicy(),
        injection_detector=InjectionDetector(),
        build_system_prompt=build_system_prompt,
        build_user_prompt=build_user_prompt,
        fallback_output=fallback_output,
    )
