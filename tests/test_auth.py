import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user():
    # Замість johndoe беремо користувача 'user', якого Alembic автоматично створює в міграції
    return {"username": "user", "password": "secret"}


def test_login_with_valid_credentials_returns_token(client, test_user):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user["username"], "password": test_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["token_type"] == "bearer"
    assert isinstance(json_data["access_token"], str)
    assert json_data["access_token"]


def test_login_with_invalid_credentials_returns_401(client, test_user):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user["username"], "password": "wrong-password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_access_to_protected_endpoint_requires_valid_token(client, test_user):
    token_response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user["username"], "password": test_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = token_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]
