from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Protocol

@dataclass(frozen=True)
class TelemetryEvent:
    ts_unix: float
    trace_id: str
    agent_name: str
    agent_version: str
    model_name: str
    latency_ms: int
    outcome: str  # success | repaired | degraded | blocked | error
    reason_code: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    estimated_cost_usd: Optional[float] = None
    meta: Optional[Dict[str, Any]] = None


class TelemetryEmitter(Protocol):
    def emit(self, event: TelemetryEvent) -> None: ...


class StdoutEmitter:
    def emit(self, event: TelemetryEvent) -> None:
        print(json.dumps(asdict(event), ensure_ascii=False))


class NullEmitter:
    def emit(self, event: TelemetryEvent) -> None:
        return


def now_unix() -> float:
    return time.time()
