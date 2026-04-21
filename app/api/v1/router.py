from fastapi import APIRouter

from .endpoints import welcome

api_router = APIRouter()

api_router.include_router(welcome.router, prefix="", tags=["Welcome"])
