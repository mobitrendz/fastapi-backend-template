import jwt
import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_current_user_malformed_token(client: AsyncClient):
    # Token with invalid signature
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.invalid_signature"  # noqa: S105
    response = await client.get(
        "/api/v1/login/current-user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_current_user_validation_error(client: AsyncClient):
    # Token with valid signature but invalid type for 'sub' (expects string or None, we give dict)
    payload = {"sub": {"invalid": "type"}, "exp": 9999999999}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    response = await client.get(
        "/api/v1/login/current-user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_read_secure_data_endpoint(client: AsyncClient, normal_user_token: str):
    response = await client.get(
        "/api/v1/login/secure-data",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 200
    assert "token" in response.json()
