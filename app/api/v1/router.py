from fastapi import APIRouter

from .endpoints import login, todos, users, welcome

api_router = APIRouter()

# Main API router that includes all endpoint routers for the application. This router is used in the main application to organize and include all the different API endpoints under a common prefix (e.g., /api/v1). Each endpoint router is responsible for handling specific functionality, such as user management, authentication, and welcome messages.
api_router.include_router(welcome.router, prefix="", tags=["Welcome"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(todos.router, prefix="/todos", tags=["ToDos"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
