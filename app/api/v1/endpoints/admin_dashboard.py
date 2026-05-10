from fastapi import APIRouter

from app.api.deps import AllowSuper, AllowSuperOrAdmin
from app.crud import system_log as system_log_crud
from app.db.database import SessionDependency
from app.models.admin_dashboard import AdminDashboardReport
from app.models.system_log import SystemLogsPublic
from app.services import admin_dashboard as admin_dashboard_service

router = APIRouter()


@router.get("/stats", response_model=AdminDashboardReport)
async def read_admin_dashboard_stats(
    session: SessionDependency,
    _current_user: AllowSuperOrAdmin,
) -> AdminDashboardReport:
    """
    Retrieve user activity metrics and trends (SUPER and ADMIN users only).
    Filters out activities from non-regular users.
    """
    return await admin_dashboard_service.get_admin_dashboard_stats(session)


@router.get("/logs", response_model=SystemLogsPublic)
async def read_system_logs(
    session: SessionDependency,
    _current_user: AllowSuper,
    limit: int = 50,
    level: str | None = None,
) -> SystemLogsPublic:
    """
    Retrieve recent system error logs (SUPER users only).
    """
    return await system_log_crud.get_system_logs(
        session=session, limit=limit, level=level
    )


@router.get("/error-test")
async def trigger_error(_current_user: AllowSuper) -> None:
    """
    Deliberately trigger an error to test the global exception handler (SUPER users only).
    """
    raise ValueError("This is a deliberate test error.")
