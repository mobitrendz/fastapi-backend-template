import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_users_api_full_coverage(client: AsyncClient, superuser_token: str):
    # 1. Create User (Line 45-46)
    email = f"final_cov_{uuid.uuid4().hex[:8]}@example.com"
    response = await client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={"email": email, "password": "password123", "full_name": "Final User"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    # 2. Read Users (Line 54)
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200

    # 3. Read User by ID (Line 67-69)
    response = await client.get(
        f"/api/v1/users/byID/{user_id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200

    # 4. Read User by Email (Line 78-80)
    response = await client.get(
        f"/api/v1/users/byEmail/{email}",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200

    # 5. Update User (Line 118-120)
    response = await client.patch(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={"full_name": "Updated Final"},
    )
    assert response.status_code == 200

    # 6. Delete User (Line 130-133)
    response = await client.delete(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_role_checker_via_api(client: AsyncClient, normal_user_token: str):
    # Try to access admin-only endpoint
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 403
