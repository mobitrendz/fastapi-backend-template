from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    email: str    
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    password: str

