from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_welcome_message():
    response = client.get("/api/v1")
    assert response.status_code == 200  # noqa: S101
    assert response.json() == {"message": "Welcome User!"}  # noqa: S101


def test_get_welcome_message_user():
    response = client.get("/api/v1/Sreeraj")
    assert response.status_code == 200  # noqa: S101
    assert response.json() == {"message": "Welcome Sreeraj!"}  # noqa: S101
