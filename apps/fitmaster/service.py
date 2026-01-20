from __future__ import annotations

from typing import Any, Dict, Optional

from werkzeug.datastructures import MultiDict

from apps.ai_core.runner import AgentRunner
from apps.ai_core.telemetry import TelemetryEmitter

from apps.bioanalyze.core import AnalysisPayload, run_biometric_analysis

from .provider_factory import build_provider
from .telemetry_factory import build_emitter
from .schemas import FitMasterInput, FitMasterOutput
from .spec import build_fitmaster_spec


class FitMasterService:
    """Adapter for FitMaster execution."""

    @staticmethod
    def _to_features_pack(payload: AnalysisPayload, *, notes: Optional[str] = None) -> FitMasterInput:
        # Context minimization: we pass the already-structured inputs/results/interpretations.
        # Avoid dumping full history here; use history_summary when available.
        return FitMasterInput(
            inputs=payload.inputs,
            results=payload.results,
            interpretations=payload.interpretations,
            goal=payload.inputs.get("objetivo"),
            notes=notes,
            history_summary=None,
        )

    @staticmethod
    def run_from_form_payload(form_payload: Dict[str, Any], *, output_version: Optional[str] = None) -> FitMasterOutput:
        """End-to-end FitMaster execution using SSD AgentRunner.

        This reuses the existing Flask biometric core (`run_biometric_analysis`) without rewriting it.
        """

        # Legacy expects strings (like form POST). Convert to MultiDict[str, str].
        normalized = {}
        for k, v in (form_payload or {}).items():
            if v is None:
                continue
            normalized[k] = str(v)

        notes = normalized.pop("notes", None)

        payload = run_biometric_analysis(MultiDict(normalized))
        features_pack = FitMasterService._to_features_pack(payload, notes=notes)

        provider, model_name = build_provider()
        spec = build_fitmaster_spec(model_name=model_name, output_version=output_version)

        emitter: TelemetryEmitter = build_emitter()
        runner = AgentRunner(provider=provider, emitter=emitter)
        # AgentRunner expects dict payloads
        return runner.run(spec, features_pack.model_dump(exclude_none=True))
