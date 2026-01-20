from __future__ import annotations

from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APIClient


@pytest.fixture
def user_factory():
    User = get_user_model()

    def _create_user(**kwargs):
        password = kwargs.pop("password", "pass123")
        username = kwargs.pop("username", f"user_{uuid4().hex}")
        user = User.objects.create_user(username=username, password=password, **kwargs)
        user._plain_password = password  # type: ignore[attr-defined]
        return user

    return _create_user


@pytest.fixture
def fitmaster_payload():
    return {
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


@pytest.fixture
def get_jwt_token():
    def _get_token(client: APIClient, user) -> str:
        resp = client.post(
            "/api/v1/auth/token/",
            {"username": user.username, "password": getattr(user, "_plain_password", "pass123")},
            format="json",
        )
        assert resp.status_code == 200, resp.content
        return resp.json()["access"]

    return _get_token


@pytest.mark.django_db
@override_settings(
    FITMASTER_PLAN_THROTTLE_RATES={
        "free": {"fitmaster_run": "1/second"},
        "pro": {"fitmaster_run": "2/second"},
    }
)
def test_fitmaster_throttle_free_vs_pro(user_factory, fitmaster_payload, get_jwt_token):
    client = APIClient()

    free_user = user_factory()
    free_token = get_jwt_token(client, free_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {free_token}")

    r1 = client.post("/api/v1/fitmaster/run/", fitmaster_payload, format="json")
    r2 = client.post("/api/v1/fitmaster/run/", fitmaster_payload, format="json")

    assert r1.status_code == 200
    assert r2.status_code == 429

    pro_user = user_factory(is_staff=True)
    pro_token = get_jwt_token(client, pro_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pro_token}")

    r1p = client.post("/api/v1/fitmaster/run/", fitmaster_payload, format="json")
    r2p = client.post("/api/v1/fitmaster/run/", fitmaster_payload, format="json")
    r3p = client.post("/api/v1/fitmaster/run/", fitmaster_payload, format="json")

    assert r1p.status_code == 200
    assert r2p.status_code == 200
    assert r3p.status_code == 429
