from django.urls import path

from .views import run_fitmaster_dev

urlpatterns = [
    path("run/", run_fitmaster_dev, name="fitmaster-run-dev"),
]
