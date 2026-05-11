import time
from datetime import UTC, datetime, timedelta
from typing import Any, cast

import psutil
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.activity import UserActivity
from app.models.dashboard import (
    ActivitySummary,
    DashboardReport,
    HotEndpoint,
    ServerMetrics,
    UserStats,
)
from app.models.user import User


async def get_server_metrics() -> ServerMetrics:
    return ServerMetrics(
        cpu_usage=psutil.cpu_percent(interval=None),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage("/").percent,
        uptime_seconds=time.time() - psutil.boot_time(),
    )


async def get_application_stats(session: AsyncSession) -> DashboardReport:
    now = datetime.now(UTC)
    last_24h = now - timedelta(hours=24)

    # User Stats
    total_users_stmt = select(func.count()).select_from(User)
    total_users = (await session.execute(total_users_stmt)).scalar() or 0

    new_regs_stmt = (
        select(func.count())
        .select_from(User)
        .where(cast(Any, User.created_at) >= last_24h)
    )
    new_regs = (await session.execute(new_regs_stmt)).scalar() or 0

    active_users_stmt = (
        select(func.count(func.distinct(UserActivity.user_id)))
        .where(cast(Any, UserActivity.created_at) >= last_24h)
        .where(cast(Any, UserActivity.user_id).is_not(None))
    )
    active_users = (await session.execute(active_users_stmt)).scalar() or 0

    # Activity Stats
    total_hits_stmt = select(func.count()).select_from(UserActivity)
    total_hits = (await session.execute(total_hits_stmt)).scalar() or 0

    success_hits_stmt = (
        select(func.count())
        .select_from(UserActivity)
        .where(UserActivity.status_code >= 200)
        .where(UserActivity.status_code < 400)
    )
    success_hits = (await session.execute(success_hits_stmt)).scalar() or 0

    failure_hits = total_hits - success_hits
    success_rate = (success_hits / total_hits * 100) if total_hits > 0 else 0.0
    failure_rate = (failure_hits / total_hits * 100) if total_hits > 0 else 0.0

    # Top Endpoints
    top_endpoints_stmt = (
        select(UserActivity.path, UserActivity.method, func.count().label("count"))
        .group_by(UserActivity.path, UserActivity.method)
        .order_by(func.count().desc())
        .limit(5)
    )
    top_endpoints_result = await session.execute(top_endpoints_stmt)
    top_endpoints = [
        HotEndpoint(path=row[0], method=row[1], count=row[2])
        for row in top_endpoints_result.all()
    ]

    server_metrics = await get_server_metrics()

    return DashboardReport(
        server=server_metrics,
        users=UserStats(
            total_users=total_users,
            active_users_24h=active_users,
            new_registrations_24h=new_regs,
        ),
        activity=ActivitySummary(
            total_hits=total_hits,
            success_rate=success_rate,
            failure_rate=failure_rate,
            top_endpoints=top_endpoints,
        ),
    )
