import os

import pytest

from apps.ai_core.runner import AgentRunner, LLMResult
from apps.fitmaster.models import AgentTelemetryEvent
from apps.fitmaster.spec import build_fitmaster_spec
from apps.fitmaster.telemetry_factory import build_emitter


class _DummyProvider:
    def complete(self, *, model: str, system: str, user: str, max_tokens=None):
        return LLMResult(
            text=(
                '{'
                '"summary": "ok",'
                '"flags": [],'
                '"assumptions": [],'
                '"nutrition": {"daily_calories": 2000, "macros": {"protein_g": 150, "carbs_g": 200, "fat_g": 60}, "meals": [], "notes": null},'
                '"training": {"weekly_split": {}, "sessions": [], "notes": null},'
                '"next_steps": [],'
                '"safety": {"disclaimer": "Siempre consulta.", "contraindications": []}'
                '}'
            ),
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            estimated_cost_usd=0.01,
        )


@pytest.mark.django_db
def test_db_emitter_persists_event(monkeypatch):
    monkeypatch.setenv("AI_TELEMETRY_EMITTER", "db")
    monkeypatch.setenv("FITMASTER_OUTPUT_VERSION", "v2")

    provider = _DummyProvider()
    emitter = build_emitter()
    runner = AgentRunner(provider=provider, emitter=emitter)
    spec = build_fitmaster_spec(model_name="dummy")

    payload = {
        "inputs": {"peso": 80, "altura": 180, "edad": 30, "genero": "h"},
        "results": {"imc": 24.5},
        "interpretations": {"imc": "normal"},
    }

    before = AgentTelemetryEvent.objects.count()
    runner.run(spec, payload)

    assert AgentTelemetryEvent.objects.count() == before + 1
