from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Protocol, Type

from pydantic import BaseModel

from .policies import (
    BudgetPolicy,
    InjectionDetector,
    PolicyViolation,
    enforce_budget_input,
    enforce_budget_output,
)
from .schemas import AgentSchemaError, schema_json, validate_model, validate_model_from_json
from .telemetry import NullEmitter, TelemetryEmitter, TelemetryEvent, now_unix


class ModelProvider(Protocol):
    """
    Adapter interface for any LLM backend (Claude/Gemini/OpenAI/DeepSeek/etc).
    Must be framework-agnostic.
    """

    def complete(self, *, model: str, system: str, user: str, max_tokens: Optional[int] = None) -> "LLMResult":
        ...


@dataclass(frozen=True)
class LLMResult:
    text: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    estimated_cost_usd: Optional[float] = None


@dataclass(frozen=True)
class AgentSpec:
    name: str
    version: str
    model_name: str
    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    budget: BudgetPolicy
    injection_detector: InjectionDetector
    build_system_prompt: Callable[[], str]
    build_user_prompt: Callable[[BaseModel], str]
    fallback_output: Callable[[str], BaseModel]  # reason -> output model instance


class ReasonCode:
    OK = "ok"
    REPAIRED = "repaired"
    REPAIR_ATTEMPT = "repair_attempt"
    BLOCKED_INJECTION = "blocked_injection"
    BLOCKED_BUDGET_INPUT = "blocked_budget_input"
    BLOCKED_BUDGET_OUTPUT = "blocked_budget_output"
    INVALID_INPUT_SCHEMA = "invalid_input_schema"
    INVALID_OUTPUT_SCHEMA = "invalid_output_schema"
    MODEL_ERROR = "model_error"
    FALLBACK = "fallback"


class AgentRunner:
    def __init__(self, provider: ModelProvider, emitter: Optional[TelemetryEmitter] = None) -> None:
        self.provider = provider
        self.emitter = emitter or NullEmitter()

    def run(self, spec: AgentSpec, payload: Dict[str, Any]) -> BaseModel:
        trace_id = uuid.uuid4().hex
        started = time.perf_counter()

        # 1) Validate input (L2)
        try:
            input_obj = validate_model(spec.input_model, payload)
        except AgentSchemaError as exc:
            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="degraded",
                reason_code=ReasonCode.INVALID_INPUT_SCHEMA,
                model_name=spec.model_name,
                err=str(exc),
            )

        # Optional: treat some free text fields as user-provided text to check budgets/injection.
        user_text = self._extract_user_text(payload)
        try:
            enforce_budget_input(user_text, spec.budget)
        except PolicyViolation as exc:
            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="blocked",
                reason_code=ReasonCode.BLOCKED_BUDGET_INPUT,
                model_name=spec.model_name,
                err=str(exc),
            )

        if spec.injection_detector.detect(user_text):
            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="blocked",
                reason_code=ReasonCode.BLOCKED_INJECTION,
                model_name=spec.model_name,
                err="prompt_injection_detected",
            )

        # 2) Call model
        system = spec.build_system_prompt()
        user = spec.build_user_prompt(input_obj)

        try:
            result = self.provider.complete(
                model=spec.model_name,
                system=system,
                user=user,
                max_tokens=spec.budget.max_tokens,
            )
        except Exception as exc:  # keep provider exceptions contained
            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="error",
                reason_code=ReasonCode.MODEL_ERROR,
                model_name=spec.model_name,
                err=str(exc),
            )

        # 3) Enforce output budget (L4 proxy)
        try:
            enforce_budget_output(result.text, spec.budget)
        except PolicyViolation as exc:
            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="blocked",
                reason_code=ReasonCode.BLOCKED_BUDGET_OUTPUT,
                model_name=spec.model_name,
                err=str(exc),
                tokens=result,
            )

        # 4) Validate output JSON (L5)
        try:
            output_obj = validate_model_from_json(spec.output_model, result.text)
            self._emit(
                spec=spec,
                trace_id=trace_id,
                started=started,
                model_name=spec.model_name,
                outcome="success",
                reason_code=ReasonCode.OK,
                tokens=result,
            )
            return output_obj
        except AgentSchemaError as exc:
            # 5) Repair attempt (1 retry)
            repaired, repair_tokens = self._attempt_repair(
                spec=spec,
                input_obj=input_obj,
                bad_output=result.text,
                error=str(exc),
                trace_id=trace_id,
            )
            if repaired is not None and repair_tokens is not None:
                self._emit(
                    spec=spec,
                    trace_id=trace_id,
                    started=started,
                    model_name=spec.model_name,
                    outcome="repaired",
                    reason_code=ReasonCode.REPAIRED,
                    tokens=self._sum_tokens(result, repair_tokens),
                    meta={"note": "repair_attempt_success", "repair_calls": 2},
                )
                return repaired

            return self._emit_and_fallback(
                spec=spec,
                trace_id=trace_id,
                started=started,
                outcome="degraded",
                reason_code=ReasonCode.INVALID_OUTPUT_SCHEMA,
                model_name=spec.model_name,
                err=str(exc),
                tokens=result,
            )

    def _attempt_repair(
        self,
        *,
        spec: AgentSpec,
        input_obj: BaseModel,
        bad_output: str,
        error: str,
        trace_id: str,
    ) -> tuple[Optional[BaseModel], Optional[LLMResult]]:
        repair_system = spec.build_system_prompt()
        expected_schema = schema_json(spec.output_model)
        repair_user = (
            "Your previous answer did not match the required JSON schema.\n"
            "Return ONLY valid JSON that matches the schema. Do not include markdown.\n\n"
            f"Schema:\n{expected_schema}\n\n"
            f"Validation error:\n{error}\n\n"
            f"Bad output:\n{bad_output}\n\n"
            "Now produce the corrected JSON:"
        )

        repair_started = time.perf_counter()
        try:
            repaired = self.provider.complete(
                model=spec.model_name,
                system=repair_system,
                user=repair_user,
                max_tokens=spec.budget.max_tokens,
            )

            # Emit repair telemetry with its own latency/tokens.
            repair_latency_ms = int((time.perf_counter() - repair_started) * 1000)
            self.emitter.emit(
                TelemetryEvent(
                    ts_unix=now_unix(),
                    trace_id=trace_id,
                    agent_name=spec.name,
                    agent_version=spec.version,
                    model_name=spec.model_name,
                    latency_ms=repair_latency_ms,
                    outcome=ReasonCode.REPAIR_ATTEMPT,
                    reason_code=ReasonCode.REPAIR_ATTEMPT,
                    prompt_tokens=repaired.prompt_tokens,
                    completion_tokens=repaired.completion_tokens,
                    total_tokens=repaired.total_tokens,
                    estimated_cost_usd=repaired.estimated_cost_usd,
                    meta={"phase": "repair"},
                )
            )

            enforce_budget_output(repaired.text, spec.budget)
            return validate_model_from_json(spec.output_model, repaired.text), repaired
        except Exception:
            return None, None

    @staticmethod
    def _sum_tokens(first: LLMResult, second: LLMResult) -> LLMResult:
        """Best-effort token aggregation (if values are present)."""

        def add(a: Optional[int], b: Optional[int]) -> Optional[int]:
            if a is None and b is None:
                return None
            return (a or 0) + (b or 0)

        def addf(a: Optional[float], b: Optional[float]) -> Optional[float]:
            if a is None and b is None:
                return None
            return (a or 0.0) + (b or 0.0)

        return LLMResult(
            text=second.text,
            prompt_tokens=add(first.prompt_tokens, second.prompt_tokens),
            completion_tokens=add(first.completion_tokens, second.completion_tokens),
            total_tokens=add(first.total_tokens, second.total_tokens),
            estimated_cost_usd=addf(first.estimated_cost_usd, second.estimated_cost_usd),
        )

    def _emit_and_fallback(
        self,
        *,
        spec: AgentSpec,
        trace_id: str,
        started: float,
        outcome: str,
        reason_code: str,
        model_name: str,
        err: str,
        tokens: Optional[LLMResult] = None,
    ) -> BaseModel:
        self._emit(
            spec=spec,
            trace_id=trace_id,
            started=started,
            model_name=model_name,
            outcome=outcome,
            reason_code=reason_code,
            tokens=tokens,
            meta={"error": err},
        )
        return spec.fallback_output(reason_code)

    def _emit(
        self,
        *,
        spec: AgentSpec,
        trace_id: str,
        started: float,
        model_name: str,
        outcome: str,
        reason_code: str,
        tokens: Optional[LLMResult],
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        latency_ms = int((time.perf_counter() - started) * 1000)
        event = TelemetryEvent(
            ts_unix=now_unix(),
            trace_id=trace_id,
            agent_name=spec.name,
            agent_version=spec.version,
            model_name=model_name,
            latency_ms=latency_ms,
            outcome=outcome,
            reason_code=reason_code,
            prompt_tokens=getattr(tokens, "prompt_tokens", None) if tokens else None,
            completion_tokens=getattr(tokens, "completion_tokens", None) if tokens else None,
            total_tokens=getattr(tokens, "total_tokens", None) if tokens else None,
            estimated_cost_usd=getattr(tokens, "estimated_cost_usd", None) if tokens else None,
            meta=meta,
        )
        self.emitter.emit(event)

    @staticmethod
    def _extract_user_text(payload: Dict[str, Any]) -> str:
        """
        Conservative extraction of free-text fields that commonly carry injection attempts.
        Extend as you define your real schemas.
        """

        parts = []
        for key in ("notes", "context", "goal", "user_message", "free_text"):
            val = payload.get(key)
            if isinstance(val, str) and val.strip():
                parts.append(val.strip())
        return "\n\n".join(parts)
