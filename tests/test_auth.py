from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_with_valid_credentials_returns_token():
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["token_type"] == "bearer"
    assert isinstance(json_data["access_token"], str)
    assert json_data["access_token"]


def test_login_with_invalid_credentials_returns_401():
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "johndoe", "password": "wrong-password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_access_to_protected_endpoint_requires_valid_token():
    token_response = client.post(
        "/api/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = token_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
