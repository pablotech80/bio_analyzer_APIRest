from __future__ import annotations

import os

from apps.ai_core.telemetry import NullEmitter, StdoutEmitter, TelemetryEmitter


def build_emitter() -> TelemetryEmitter:
    name = os.getenv("AI_TELEMETRY_EMITTER", "stdout").strip().lower()

    if name in ("stdout", "console"):
        return StdoutEmitter()

    if name in ("null", "none", "off"):
        return NullEmitter()

    # Default safe choice
    return StdoutEmitter()
