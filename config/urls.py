from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.urls import include


def health(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("bioanalyze/", include("apps.bioanalyze.urls")),
    path("fitmaster/", include("apps.fitmaster.urls")),
]
