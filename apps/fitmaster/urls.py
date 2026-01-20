from django.urls import path

from .views import run_fitmaster

urlpatterns = [
    path("run/", run_fitmaster, name="fitmaster-run"),
]
