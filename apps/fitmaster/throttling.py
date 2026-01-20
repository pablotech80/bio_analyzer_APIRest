from __future__ import annotations

from typing import Any, Dict, Optional

from django.conf import settings
from rest_framework.throttling import ScopedRateThrottle


class PlanScopedRateThrottle(ScopedRateThrottle):
    """Scoped throttle that selects per-plan rate limits for FitMaster endpoints."""

    def allow_request(self, request, view):  # type: ignore[override]
        self.request = request
        return super().allow_request(request, view)

    def _resolve_plan(self, user: Any) -> str:
        plan = getattr(user, "plan", None)
        if isinstance(plan, str) and plan.strip():
            return plan.strip().lower()

        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return "pro"
        return "free"

    def _plan_scope_rates(self) -> Dict[str, Dict[str, str]]:
        raw_rates: Optional[Dict[str, Dict[str, str]]] = getattr(
            settings, "FITMASTER_PLAN_THROTTLE_RATES", None
        )
        return raw_rates or {}

    def get_rate(self) -> Optional[str]:  # type: ignore[override]
        if not getattr(self, "scope", None):
            return super().get_rate()

        request = getattr(self, "request", None)
        user = getattr(request, "user", None) if request else None

        if not user or not getattr(user, "is_authenticated", False):
            return super().get_rate()

        plan = self._resolve_plan(user)
        plan_rates = self._plan_scope_rates().get(plan, {})

        rate = plan_rates.get(self.scope)
        if rate:
            return rate

        return super().get_rate()
