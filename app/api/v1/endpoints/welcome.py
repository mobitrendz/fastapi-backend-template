from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.config import settings
from app.db.database import SessionDependency

router = APIRouter()


@router.get("/checkDBConnection", response_model=dict[str, str])
def check_database_connection(session: SessionDependency) -> dict[str, str]:
    try:
        session.exec(select(1))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        ) from e


@router.get("/getEnvironment", response_model=dict[str, str])
def get_env_settings() -> dict[str, str]:
    return {"Environment": settings.ENVIRONMENT}


@router.get("/{user_name}", response_model=dict[str, str])
def get_custom_welcome_message(user_name: str) -> dict[str, str]:
    return {"message": "Welcome " + user_name + "!"}


@router.get("/", response_model=dict[str, str])
def get_welcome_message() -> dict[str, str]:
    return {"message": "Welcome User!"}
