import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_dashboard_stats_superuser(
    client: AsyncClient, superuser_token: str
):
    response = await client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "server" in data
    assert "users" in data
    assert "activity" in data
    assert "cpu_usage" in data["server"]
    assert "total_users" in data["users"]


@pytest.mark.asyncio
async def test_read_dashboard_stats_admin_denied(
    client: AsyncClient, admin_user_token: str
):
    response = await client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_dashboard_stats_user_denied(
    client: AsyncClient, normal_user_token: str
):
    response = await client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_dashboard_stats_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/dashboard/stats")
    assert response.status_code == 401
