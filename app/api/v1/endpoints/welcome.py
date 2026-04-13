from fastapi import APIRouter, HTTPException
from sqlmodel import text

from app.core.config import settings
from app.db.database import SessionDependency

router = APIRouter()

@router.get("/checkDBConnection")
def check_database_connection(session: SessionDependency):
    try:
        session.exec(text("SELECT 1"))  # ty:ignore[no-matching-overload]
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}") 

@router.get("/getEnvironment")
def get_env_settings():
    return {"Environment": settings.ENVIRONMENT}

@router.get("/{user_name}")
def get_custom_welcome_message(user_name: str):
    return {"message": "Welcome " + user_name + "!"}

@router.get("/")
def get_welcome_message():
    return {"message": "Welcome User!"}