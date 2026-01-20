from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FitMasterSpec:
    name: str = "fitmaster"
    version: str = "0.1"
