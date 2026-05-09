from sqlmodel import SQLModel


class ServerMetrics(SQLModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    uptime_seconds: float


class UserStats(SQLModel):
    total_users: int
    active_users_24h: int
    new_registrations_24h: int


class HotEndpoint(SQLModel):
    path: str
    method: str
    count: int


class ActivitySummary(SQLModel):
    total_hits: int
    success_rate: float
    failure_rate: float
    top_endpoints: list[HotEndpoint]


class DashboardReport(SQLModel):
    server: ServerMetrics
    users: UserStats
    activity: ActivitySummary
