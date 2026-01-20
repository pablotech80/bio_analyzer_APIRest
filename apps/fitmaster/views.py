from __future__ import annotations

import os

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from .serializers import FitMasterRunSerializer
from .service import FitMasterService


@api_view(["POST"])
def run_fitmaster(request: Request):
    enabled = os.getenv("ENABLE_FITMASTER_DEV_ENDPOINT", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

    if not settings.DEBUG or not enabled:
        return JsonResponse({"detail": "Not found"}, status=404)

    serializer = FitMasterRunSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    result = FitMasterService.run_from_form_payload(serializer.validated_data)

    return JsonResponse(result.model_dump(exclude_none=True), status=200)
