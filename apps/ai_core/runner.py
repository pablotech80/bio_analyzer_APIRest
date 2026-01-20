from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class AgentRequest:
    agent_name: str
    input: Dict[str, Any]
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass(frozen=True)
class AgentResult:
    output: Dict[str, Any]
    blocked: bool = False
    reason: Optional[str] = None
    metadata: Dict[str, Any] | None = None


class AgentRunner:
    """Framework-agnostic runner. No Django imports allowed."""

    def __init__(self, policy_engine: Any, telemetry: Any):
        self._policy_engine = policy_engine
        self._telemetry = telemetry

    def run(self, request: AgentRequest, agent: Any) -> AgentResult:
        # Placeholders for Bloque 2 (L2/L5/L6)
        decision = self._policy_engine.evaluate(request)
        if decision.blocked:
            self._telemetry.record_blocked(request, decision)
            return AgentResult(output={}, blocked=True, reason=decision.reason, metadata={})

        self._telemetry.record_start(request)
        raw_output = agent.execute(request)
        self._telemetry.record_success(request)
        return AgentResult(output=raw_output, blocked=False, reason=None, metadata={})
