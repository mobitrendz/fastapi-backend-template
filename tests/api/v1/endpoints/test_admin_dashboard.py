import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_admin_dashboard_stats_admin(
    client: AsyncClient, admin_user_token: str
):
    response = await client.get(
        "/api/v1/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_regular_users" in data
    assert "daily_trends" in data
    assert "top_active_users" in data


@pytest.mark.asyncio
async def test_read_admin_dashboard_stats_superuser(
    client: AsyncClient, superuser_token: str
):
    response = await client.get(
        "/api/v1/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_admin_dashboard_stats_user_denied(
    client: AsyncClient, normal_user_token: str
):
    response = await client.get(
        "/api/v1/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_admin_dashboard_stats_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/admin/dashboard/stats")
    assert response.status_code == 401
