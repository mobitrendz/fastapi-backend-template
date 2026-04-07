import uuid
from pydantic import EmailStr
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime

def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)  
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)  


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime | None