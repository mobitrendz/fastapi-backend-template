import uuid
from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from app.models.user import get_datetime_utc


class ToDoStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


class ToDoPriority(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ToDoListBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: ToDoStatus = Field(default=ToDoStatus.PENDING)
    due_date_time: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    priority: ToDoPriority = Field(default=ToDoPriority.MEDIUM)


class ToDoListCreate(ToDoListBase):
    pass


class ToDoListUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: ToDoStatus | None = None
    due_date_time: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    priority: ToDoPriority | None = None


class ToDoList(ToDoListBase, table=True):
    __tablename__: ClassVar[str] = "todo_list"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ToDoListPublic(ToDoListBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class ToDoListsPublic(SQLModel):
    data: list[ToDoListPublic]
    count: int
