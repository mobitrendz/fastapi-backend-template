from fastapi import APIRouter

from app.api.deps import AllowSuperOrAdmin
from app.db.database import SessionDependency
from app.models.admin_dashboard import AdminDashboardReport
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
