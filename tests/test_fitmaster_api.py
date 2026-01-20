import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from uuid import uuid4

from apps.fitmaster.models import AgentTelemetryEvent


@pytest.mark.django_db
def test_fitmaster_run_requires_auth(monkeypatch):
    monkeypatch.setenv("AI_TELEMETRY_EMITTER", "db")
    monkeypatch.setenv("FITMASTER_OUTPUT_VERSION", "v2")
    monkeypatch.setenv("AI_PROVIDER", "dummy")

    client = APIClient()

    payload = {
        "peso": 80,
        "altura": 180,
        "edad": 30,
        "genero": "h",
        "cuello": 40,
        "cintura": 85,
        "factor_actividad": 1.55,
        "objetivo": "perder grasa",
        "nivel": "intermedio",
        "notes": "test",
    }

    before = AgentTelemetryEvent.objects.count()
    resp = client.post("/api/v1/fitmaster/run/", payload, format="json")

    assert resp.status_code == 401
    assert AgentTelemetryEvent.objects.count() == before


@pytest.mark.django_db
def test_fitmaster_run_authenticated_persists_telemetry(monkeypatch):
    monkeypatch.setenv("AI_TELEMETRY_EMITTER", "db")
    monkeypatch.setenv("FITMASTER_OUTPUT_VERSION", "v2")
    monkeypatch.setenv("AI_PROVIDER", "dummy")

    User = get_user_model()
    user = User.objects.create_user(username=f"u_{uuid4().hex}", password="pass123")

    client = APIClient()

    token_resp = client.post(
        "/api/v1/auth/token/",
        {"username": user.username, "password": "pass123"},
        format="json",
    )
    assert token_resp.status_code == 200
    access_token = token_resp.json()["access"]

    payload = {
        "peso": 80,
        "altura": 180,
        "edad": 30,
        "genero": "h",
        "cuello": 40,
        "cintura": 85,
        "factor_actividad": 1.55,
        "objetivo": "perder grasa",
        "nivel": "intermedio",
        "notes": "test",
    }

    before = AgentTelemetryEvent.objects.count()
    resp = client.post(
        "/api/v1/fitmaster/run/",
        payload,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )

    assert resp.status_code == 200
    assert AgentTelemetryEvent.objects.count() == before + 1
