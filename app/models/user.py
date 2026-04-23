import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from app.crud import user as user_crud

# User model and related schemas for user management, including role-based access control dependencies. This module defines the User model for database interactions, as well as Pydantic models for user creation, updating, and public representation. It also includes role-based access control dependencies to enforce permissions on API endpoints.
# The User model includes fields for ID, full name, email, hashed password, active status, role, and creation timestamp. The related schemas ensure that the necessary fields are provided for user creation and updating, and that sensitive information like the hashed password is not exposed in API responses. The role-based access control dependencies allow for fine-grained control over which users can access certain endpoints based on their assigned role (admin, user, guest).
# The get_datetime_utc function ensures that all timestamps are stored in UTC, providing consistency across different timezones. The RoleChecker class is a reusable dependency that checks if the current user's role is in the allowed roles for a given endpoint, raising an HTTP 403 error if they do not have the necessary permissions.
# The UserPublic model is used for API responses to ensure that only non-sensitive information is returned, while the UsersPublic model provides a structure for returning a list of users along with a count of the total number of users. The AllowAdmin, AllowUser, and AllowAdminAndUser dependencies can be used in API endpoints to enforce role-based access control based on the user's role.
# The code is organized to separate concerns, with the User model handling database interactions and the related schemas and dependencies handling API input validation and access control. This structure promotes maintainability and scalability as the application grows.

# Function to get the current UTC datetime, used for setting the created_at field in the User model. This ensures that all timestamps are stored in a consistent timezone (UTC) regardless of the server's local timezone.
def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# User roles for role-based access control
class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# Base model for user, including common fields and validation. This model is used as a base for both the UserCreate and UserPublic models, ensuring consistency in the fields and validation across different user-related operations.
class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER)  # Defaults to standard user


# UserCreate model for creating new users, including password validation. This model is used in the user creation endpoint to ensure that the necessary fields are provided and that the password meets the specified length requirements.
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


# UserUpdate model for updating user information, allowing changes to the full name. This model is used in the update endpoint to specify which fields can be updated by the user or admin.
class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)


# User model representing the database table, including fields for ID, hashed password, and creation timestamp. This model is used for database operations and includes validation and constraints.
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None

# Response model for returning a list of users along with the total count. This is used in the endpoint that retrieves all users, providing both the user data and metadata about the number of users returned.
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int



# Role-based access control dependencies
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Annotated[User, Depends(user_crud.get_current_user)]) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the necessary permissions."
            )
        return current_user


# Define access levels
ALLOW_ADMIN = RoleChecker([UserRole.ADMIN])
ALLOW_USER = RoleChecker([UserRole.USER])
ALLOW_ADMIN_AND_USER = RoleChecker([UserRole.ADMIN, UserRole.USER])


# Define a reusable type alias
AllowAdmin = Annotated[User, Depends(ALLOW_ADMIN)]
AllowlUser = Annotated[User, Depends(ALLOW_USER)]
AllowAdminAndUser = Annotated[User, Depends(ALLOW_ADMIN_AND_USER)]
