from fastapi import APIRouter

from .endpoints import login, users, welcome

api_router = APIRouter()

api_router.include_router(welcome.router, prefix="", tags=["Welcome"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
