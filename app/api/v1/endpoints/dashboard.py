from fastapi import APIRouter

from app.api.deps import AllowSuper
from app.db.database import SessionDependency
from app.models.dashboard import DashboardReport
from app.services import dashboard as dashboard_service

router = APIRouter()


@router.get("/stats", response_model=DashboardReport)
async def read_dashboard_stats(
    session: SessionDependency,
    _current_user: AllowSuper,
) -> DashboardReport:
    """
    Retrieve comprehensive system and application metrics (SUPER users only).
    """
    return await dashboard_service.get_application_stats(session)
