from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False

class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class UserCreate(UserBase):
    pass