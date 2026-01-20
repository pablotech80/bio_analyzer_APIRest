from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.fitmaster.views import FitMasterRunAPIView


def health(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/fitmaster/run/", FitMasterRunAPIView.as_view()),
    path("bioanalyze/", include("apps.bioanalyze.urls")),
    path("fitmaster/", include("apps.fitmaster.urls")),
]
