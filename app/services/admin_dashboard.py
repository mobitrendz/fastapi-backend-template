from datetime import UTC, datetime, timedelta
from typing import Any, cast

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.activity import UserActivity
from app.models.admin_dashboard import (
    AdminDashboardReport,
    DailyActivity,
    UserActivityStat,
)
from app.models.user import User, UserRole


async def get_admin_dashboard_stats(session: AsyncSession) -> AdminDashboardReport:
    now = datetime.now(UTC)
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    # 1. Total Regular Users
    user_count_stmt = (
        select(func.count()).select_from(User).where(User.role == UserRole.USER)
    )
    total_regular_users = (await session.execute(user_count_stmt)).scalar() or 0

    # 2. Total Activities for regular users in last 24h
    activity_24h_stmt = (
        select(func.count())
        .select_from(UserActivity)
        .join(User, cast(Any, UserActivity.user_id) == User.id)
        .where(User.role == UserRole.USER)
        .where(cast(Any, UserActivity.created_at) >= last_24h)
    )
    total_activities_24h = (await session.execute(activity_24h_stmt)).scalar() or 0

    # 3. Daily Trends (last 7 days)
    # Note: Using DATE(created_at) for grouping
    daily_trends_stmt = (
        select(
            func.date(cast(Any, UserActivity.created_at)).label("date"),
            func.count().label("count"),
        )
        .join(User, cast(Any, UserActivity.user_id) == User.id)
        .where(User.role == UserRole.USER)
        .where(cast(Any, UserActivity.created_at) >= last_7d)
        .group_by(func.date(cast(Any, UserActivity.created_at)))
        .order_by("date")
    )
    daily_trends_result = await session.execute(daily_trends_stmt)
    daily_trends = [
        DailyActivity(date=row[0], count=row[1]) for row in daily_trends_result.all()
    ]

    # 4. Top Active Users
    top_users_stmt = (
        select(User.email, User.full_name, func.count().label("count"))
        .join(UserActivity, User.id == cast(Any, UserActivity.user_id))
        .where(User.role == UserRole.USER)
        .group_by(User.email, cast(Any, User.full_name))
        .order_by(func.count().desc())
        .limit(10)
    )
    top_users_result = await session.execute(top_users_stmt)
    top_active_users = [
        UserActivityStat(email=row[0], full_name=row[1], count=row[2])
        for row in top_users_result.all()
    ]

    return AdminDashboardReport(
        total_regular_users=total_regular_users,
        total_activities_24h=total_activities_24h,
        daily_trends=daily_trends,
        top_active_users=top_active_users,
    )
