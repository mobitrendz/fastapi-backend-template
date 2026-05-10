import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as user_crud
from app.crud.activity import create_activity, get_user_activities
from app.models.user import UserCreate, UserRole
from app.services.admin_dashboard import get_admin_dashboard_stats
from app.services.dashboard import get_application_stats, get_server_metrics


@pytest.mark.asyncio
async def test_dashboard_service_direct(session: AsyncSession):
    # Ensure some data exists
    user_in = UserCreate(
        email=f"test_dash_{uuid.uuid4().hex[:6]}@example.com",
        password="password123",
        full_name="Dash User",
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    # Create some activity
    await create_activity(
        session=session,
        user_id=user.id,
        method="GET",
        path="/api/v1/test",
        status_code=200,
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    stats = await get_application_stats(session)
    assert stats.users.total_users >= 1
    assert stats.activity.total_hits >= 1
    assert len(stats.activity.top_endpoints) >= 1


@pytest.mark.asyncio
async def test_admin_dashboard_service_direct(session: AsyncSession):
    # Ensure a regular user exists
    user_in = UserCreate(
        email=f"test_admin_dash_{uuid.uuid4().hex[:6]}@example.com",
        password="password123",
        full_name="Regular User",
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    # Create some activity for this regular user
    await create_activity(
        session=session,
        user_id=user.id,
        method="POST",
        path="/api/v1/todos",
        status_code=201,
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    stats = await get_admin_dashboard_stats(session)
    assert stats.total_regular_users >= 1
    assert stats.total_activities_24h >= 1
    assert len(stats.top_active_users) >= 1


@pytest.mark.asyncio
async def test_activity_crud_direct(session: AsyncSession):
    # Create a real user first to avoid FK violation
    user_in = UserCreate(
        email=f"activity_test_{uuid.uuid4().hex[:6]}@example.com",
        password="password123",
        full_name="Activity Test User",
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    # Create activity
    activity = await create_activity(
        session=session,
        user_id=user.id,
        method="PUT",
        path="/api/v1/update",
        status_code=204,
        ip_address="1.1.1.1",
        user_agent="direct-test",
    )
    assert activity.method == "PUT"
    assert activity.user_id == user.id

    # Get activities
    activities = await get_user_activities(session=session, user_id=user.id)
    assert activities.count == 1
    assert activities.data[0].path == "/api/v1/update"


@pytest.mark.asyncio
async def test_server_metrics_direct():
    metrics = await get_server_metrics()
    assert 0 <= metrics.cpu_usage <= 100
    assert 0 <= metrics.memory_usage <= 100
    assert metrics.uptime_seconds > 0
