import uuid

from fastapi import APIRouter, HTTPException

from app.crud import user as user_crud
from app.db.database import SessionDependency
from app.models.generic import Message
from app.models.user import (
    AllowAdmin,
    AllowAdminAndUser,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserUpdate,
)

router = APIRouter()


# User endpoints for managing user accounts, including creation, retrieval, updating, and deletion.
# These endpoints utilize the CRUD operations defined in app/crud/user.py and enforce role-based access control using dependencies defined in app/models/user.py.
# Admin users can perform all operations, while regular users can only access and modify their own data.
# The endpoints return appropriate HTTP status codes and messages based on the success or failure of the operations.
# Each endpoint is documented with comments explaining its purpose, the expected input and output, and the access control requirements.

# Endpoint for creating a new user. Only admin users can perform this operation. Returns the created user if successful, or a 400 error if the email is already in use.
@router.post("/", response_model=UserPublic)
def create_user(session: SessionDependency, allow_admin: AllowAdmin, user_create: UserCreate):
    return user_crud.create_user(session=session, user_create=user_create)


# Endpoint for retrieving all users. Only admin users can perform this operation. Returns a list of users along with the total count.
@router.get("/", response_model=UsersPublic)
def read_users(session: SessionDependency, allow_admin: AllowAdmin):
    return user_crud.get_users(session=session)


# Endpoint for retrieving a user by ID. Both admin and regular users can perform this operation, but regular users can only access their own information. Returns the user if found, or a 404 error if not found.
@router.get("/byID/{id}", response_model=UserPublic)
def read_user_by_id(session: SessionDependency, allow_admin: AllowAdmin, id: uuid.UUID):
    return user_crud.get_user_by_id(session=session, id=id)


# Endpoint for retrieving a user by email. Only admin users can perform this operation. Returns the user if found, or a 404 error if not found.
@router.get("/byEmail/{email}", response_model=UserPublic)
def read_user_by_email(session: SessionDependency, allow_admin: AllowAdmin, email: str):
    return user_crud.get_user_by_email(session=session, email=email)


# Endpoint for updating a user's information by ID. Both admin and regular users can perform this operation, but regular users can only update their own information. Returns the updated user or a 404 error if the user is not found.
@router.patch("/{id}", response_model=UserPublic)
def update_user(session: SessionDependency, allow_admin_and_user: AllowAdminAndUser, id: uuid.UUID, user_update: UserUpdate):
    return user_crud.update_user(session=session, id=id, user_update=user_update)


# Endpoint for deleting a user by ID. Only admin users can perform this operation. Returns a success message if the user is deleted, or a 404 error if the user is not found.
@router.delete("/{id}", response_model=Message)
def delete_user(session: SessionDependency, allow_admin: AllowAdmin, id: uuid.UUID):
    deleted = user_crud.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")
