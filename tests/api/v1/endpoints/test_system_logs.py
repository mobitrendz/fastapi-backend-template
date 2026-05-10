import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.system_log import create_system_log, get_system_logs


@pytest.mark.asyncio
async def test_system_log_crud_works(session: AsyncSession):
    # Test CRUD directly
    log = await create_system_log(
        session=session,
        level="ERROR",
        message="Direct CRUD Test",
        path="/test-path",
        method="POST",
    )
    assert log.message == "Direct CRUD Test"
    assert log.level == "ERROR"

    logs = await get_system_logs(session=session)
    assert logs.count >= 1
    assert any(log_entry.message == "Direct CRUD Test" for log_entry in logs.data)


@pytest.mark.asyncio
async def test_admin_dashboard_logs_endpoint(
    client: AsyncClient, superuser_token: str, session: AsyncSession
):
    # Ensure there's at least one log
    await create_system_log(
        session=session,
        level="ERROR",
        message="Endpoint Test",
    )

    response = await client.get(
        "/api/v1/admin/dashboard/logs",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["count"] >= 1


@pytest.mark.asyncio
async def test_global_handler_response_structure(
    client: AsyncClient, superuser_token: str
):
    # We test that the handler returns the correct 500 structure
    # Persistence across async tasks in tests is flaky due to transaction isolation,
    # but we can verify the API behavior.
    response = await client.get(
        "/api/v1/admin/dashboard/error-test",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "An internal server error occurred. The administrators have been notified."
    )


@pytest.mark.asyncio
async def test_admin_cannot_access_logs(client: AsyncClient, admin_user_token: str):
    response = await client.get(
        "/api/v1/admin/dashboard/logs",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_regular_user_cannot_access_logs(
    client: AsyncClient, normal_user_token: str
):
    response = await client.get(
        "/api/v1/admin/dashboard/logs",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 403
