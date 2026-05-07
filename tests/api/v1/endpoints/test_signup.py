import secrets

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as user_crud
from app.models.user import UserCreate, UserRole


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient):
    email = f"signup_{secrets.token_hex(4)}@example.com"
    full_name = "New User"
    password = "password123"  # noqa: S105

    response = await client.post(
        "/api/v1/login/signup",
        json={
            "email": email,
            "full_name": full_name,
            "password": password,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["full_name"] == full_name
    assert "id" in data
    assert "role" in data
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_signup_existing_email(client: AsyncClient, session: AsyncSession):
    # Ensure user exists
    user_in = UserCreate(
        full_name="Existing User",
        email="user@example.com",
        password="password123",  # noqa: S106
        role=UserRole.USER,
    )
    await user_crud.create_user(session=session, user_create=user_in)

    response = await client.post(
        "/api/v1/login/signup",
        json={
            "email": "user@example.com",
            "full_name": "Another User",
            "password": "password123",  # noqa: S105
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"
