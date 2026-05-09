import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


# Function to get the current UTC datetime
def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# User roles for role-based access control
class UserRole(StrEnum):
    SUPER = "super"  # System-level administrator
    ADMIN = "admin"  # Staff administrator
    USER = "user"  # End user (only role with ToDo access)


# Base model for user, including common fields.
class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER)


# UserCreate model for creating new users (used by SUPER/ADMIN)
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


# UserRegister model for public self-registration (defaults to USER role)
class UserRegister(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)


# UserUpdate model for updating user information
class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool | None = Field(default=None)
    role: UserRole | None = Field(default=None)


# UpdatePassword model for changing a user's password
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# User model representing the database table
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Properties to return via API
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


# Response model for list of users
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
