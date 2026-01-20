import os
import unittest

import pytest

from apps.ai_core.runner import AgentRunner
from apps.ai_core.telemetry import NullEmitter
from apps.fitmaster.spec import build_fitmaster_spec
from apps.fitmaster.provider_factory import build_provider


@pytest.mark.integration
class TestOpenAIIntegration(unittest.TestCase):
    def test_openai_real_call_optional(self):
        if os.getenv("AI_PROVIDER") != "openai" or not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI integration test requires AI_PROVIDER=openai and OPENAI_API_KEY")

        provider, model_name = build_provider()
        runner = AgentRunner(provider=provider, emitter=NullEmitter())
        spec = build_fitmaster_spec(model_name=model_name)

        payload = {
            "inputs": {"peso": 80, "altura": 180, "edad": 30, "genero": "h"},
            "results": {"imc": 24.7, "tmb": 1700, "tdee": 2600},
            "interpretations": {"imc": "normal"},
            "notes": "Devuelve una interpretación breve y un plan básico.",
        }

        out = runner.run(spec, payload)
        assert isinstance(out.summary, str)
        assert len(out.summary) > 0
