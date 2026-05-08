import uuid

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlmodel import select

from app.crud import user as user_crud
from app.crud.user import AllowAdmin, AllowAdminAndUser, CurrentUser
from app.db.database import SessionDependency
from app.models.generic import Message
from app.models.user import (
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRole,
    UserUpdate,
)

disable_installed_extensions_check()

router = APIRouter()


# User endpoints for managing user accounts, including creation, retrieval, updating, and deletion.
# These endpoints utilize the CRUD operations defined in app/crud/user.py and enforce role-based access control using dependencies defined in app/models/user.py.
# Admin users can perform all operations, while regular users can only access and modify their own data.
# The endpoints return appropriate HTTP status codes and messages based on the success or failure of the operations.
# Each endpoint is documented with comments explaining its purpose, the expected input and output, and the access control requirements.


# Endpoint for creating a new user. Only admin users can perform this operation. Returns the created user if successful, or a 400 error if the email is already in use.
@router.post("/", response_model=UserPublic)
async def create_user(
    session: SessionDependency, _allow_admin: AllowAdmin, user_create: UserCreate
) -> UserPublic:
    user = await user_crud.get_user_by_email(session=session, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )
    user = await user_crud.create_user(session=session, user_create=user_create)
    return UserPublic.model_validate(user)


# Endpoint for retrieving all users. Only admin users can perform this operation. Returns a list of users along with the total count.
@router.get("/", response_model=Page[UserPublic])
async def read_users(
    session: SessionDependency, _allow_admin: AllowAdmin
) -> Page[UserPublic]:
    return await apaginate(session, select(User))  # type: ignore


# Endpoint for retrieving a user by ID. Both admin and regular users can perform this operation, but regular users can only access their own information. Returns the user if found, or a 404 error if not found.
@router.get("/byID/{id}", response_model=UserPublic)
async def read_user_by_id(
    session: SessionDependency,
    current_user: AllowAdminAndUser,
    id: uuid.UUID,
) -> UserPublic:
    if current_user.role != UserRole.ADMIN and current_user.id != id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = await user_crud.get_user_by_id(session=session, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)


# Endpoint for retrieving a user by email. Only admin users can perform this operation. Returns the user if found, or a 404 error if not found.
@router.get("/byEmail/{email}", response_model=UserPublic)
async def read_user_by_email(
    session: SessionDependency, _allow_admin: AllowAdmin, email: str
) -> UserPublic:
    user = await user_crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)


# Endpoint for updating a user's password. Both admin and regular users can perform this operation, but regular users can only update their own password. Returns a success message if the password is updated, or a 400 error if the current password is incorrect or if the update fails.
@router.patch("/password", response_model=Message)
async def update_password(
    session: SessionDependency,
    _allow_admin_and_user: AllowAdminAndUser,
    update_password: UpdatePassword,
    current_user: CurrentUser,
) -> Message:
    password_updated = await user_crud.update_password(
        session=session, updatePassword=update_password, current_user=current_user
    )
    if password_updated:
        return Message(message="Password updated successfully")
    else:
        raise HTTPException(status_code=400, detail="Failed to update password")


# Endpoint for updating a user's information by ID. Both admin and regular users can perform this operation, but regular users can only update their own information. Admins can update any user's information, including their role and active status. Returns the updated user or a 404 error if the user is not found.
@router.patch("/{id}", response_model=UserPublic)
async def update_user(
    session: SessionDependency,
    current_user: AllowAdminAndUser,
    id: uuid.UUID,
    user_update: UserUpdate,
) -> UserPublic:
    if current_user.role != UserRole.ADMIN:
        if current_user.id != id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        if user_update.role is not None or user_update.is_active is not None:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions to update role or active status",
            )

    user = await user_crud.update_user(session=session, id=id, user_update=user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)


# Endpoint for deleting a user by ID. Only admin users can perform this operation. Returns a success message if the user is deleted, or a 404 error if the user is not found.
@router.delete("/{id}", response_model=Message)
async def delete_user(
    session: SessionDependency, _allow_admin: AllowAdmin, id: uuid.UUID
) -> Message:
    deleted = await user_crud.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")
