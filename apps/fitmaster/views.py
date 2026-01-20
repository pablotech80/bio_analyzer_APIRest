from __future__ import annotations

import os

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .serializers import FitMasterRunSerializer
from .service import FitMasterService
from .throttling import PlanScopedRateThrottle


class FitMasterRunAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "fitmaster_run"
    throttle_classes = [PlanScopedRateThrottle, UserRateThrottle]

    def post(self, request: Request) -> Response:
        serializer = FitMasterRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = FitMasterService.run_from_form_payload(
            serializer.validated_data, output_version="v2"
        )
        return Response(result.model_dump(exclude_none=True), status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([])
def run_fitmaster_dev(request: Request):
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

    version = request.query_params.get("version")
    result = FitMasterService.run_from_form_payload(serializer.validated_data, output_version=version)

    return JsonResponse(result.model_dump(exclude_none=True), status=200)
