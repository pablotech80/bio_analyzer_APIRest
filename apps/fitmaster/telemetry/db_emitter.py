from __future__ import annotations

from apps.ai_core.telemetry import TelemetryEmitter, TelemetryEvent
from apps.fitmaster.models import AgentTelemetryEvent


class DBEmitter(TelemetryEmitter):
    """Telemetry emitter that persists events using Django ORM."""

    def emit(self, event: TelemetryEvent) -> None:  # pragma: no cover - thin wrapper
        AgentTelemetryEvent.objects.create(
            ts_unix=event.ts_unix,
            trace_id=event.trace_id,
            agent_name=event.agent_name,
            agent_version=event.agent_version,
            model_name=event.model_name,
            latency_ms=event.latency_ms,
            outcome=event.outcome,
            reason_code=event.reason_code,
            prompt_tokens=event.prompt_tokens,
            completion_tokens=event.completion_tokens,
            total_tokens=event.total_tokens,
            estimated_cost_usd=event.estimated_cost_usd,
            meta=event.meta,
        )
