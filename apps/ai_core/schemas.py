from __future__ import annotations

from pydantic import BaseModel


class BaseAgentInput(BaseModel):
    """Base schema for agent inputs."""


class BaseAgentOutput(BaseModel):
    """Base schema for agent outputs."""
