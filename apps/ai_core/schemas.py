from __future__ import annotations

import json
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel, ConfigDict, ValidationError


class AgentSchemaError(Exception):
    """Raised when input/output cannot be validated against the expected schema."""


T = TypeVar("T", bound=BaseModel)


class StrictModel(BaseModel):
    """
    Base model for agent I/O.
    - extra='forbid' prevents silent schema drift
    - validate_assignment makes runtime mutations safer
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


def parse_json_strict(raw: str) -> Dict[str, Any]:
    """
    Parse JSON strictly. Raises AgentSchemaError if invalid or not an object.
    """

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AgentSchemaError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise AgentSchemaError("JSON must be an object at top level.")
    return data


def validate_model(model_cls: Type[T], payload: Dict[str, Any]) -> T:
    """
    Validate payload dict into a Pydantic model instance.
    """

    try:
        return model_cls.model_validate(payload)
    except ValidationError as exc:
        raise AgentSchemaError(str(exc)) from exc


def validate_model_from_json(model_cls: Type[T], raw_json: str) -> T:
    """
    Parse + validate JSON into a Pydantic model instance.
    """

    payload = parse_json_strict(raw_json)
    return validate_model(model_cls, payload)


def schema_json(model_cls: Type[BaseModel]) -> str:
    """
    Returns JSON schema as a pretty string for repair prompts / debugging.
    """

    return json.dumps(model_cls.model_json_schema(), indent=2, ensure_ascii=False)


def dump_json(model: BaseModel) -> str:
    """
    Dump model as compact JSON (stable field order not guaranteed, but compact).
    """

    return model.model_dump_json(exclude_none=True)


class BaseAgentInput(StrictModel):
    """Base schema for agent inputs."""


class BaseAgentOutput(StrictModel):
    """Base schema for agent outputs."""
