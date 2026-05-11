from datetime import date

from sqlmodel import SQLModel


class DailyActivity(SQLModel):
    date: date
    count: int


class UserActivityStat(SQLModel):
    email: str
    full_name: str | None
    count: int


class AdminDashboardReport(SQLModel):
    total_regular_users: int
    total_activities_24h: int
    daily_trends: list[DailyActivity]
    top_active_users: list[UserActivityStat]
