from __future__ import annotations

from typing import Any


class Telemetry:
    """Framework-agnostic telemetry interface. No Django imports allowed."""

    def record_start(self, _request: Any) -> None:
        return None

    def record_success(self, _request: Any) -> None:
        return None

    def record_blocked(self, _request: Any, _decision: Any) -> None:
        return None
