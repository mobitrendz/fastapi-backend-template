import uuid

from fastapi import APIRouter, HTTPException

from app.crud import user as user_crud
from app.db.database import SessionDependency
from app.models.generic import Message
from app.models.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(session: SessionDependency, user_create: UserCreate):
    return user_crud.create_user(session=session, user_create=user_create)


@router.get("/", response_model=list[UserRead])
def read_users(session: SessionDependency):
    return user_crud.get_users(session=session)


@router.get("/byID/{id}", response_model=UserRead)
def read_user_by_id(session: SessionDependency, id: uuid.UUID):
    return user_crud.get_user_by_id(session=session, id=id)


@router.get("/byEmail/{email}", response_model=UserRead)
def read_user_by_email(session: SessionDependency, email: str):
    return user_crud.get_user_by_email(session=session, email=email)


@router.patch("/{id}", response_model=UserRead)
def update_user(session: SessionDependency, id: uuid.UUID, user_update: UserUpdate):
    return user_crud.update_user(session=session, id=id, user_update=user_update)


@router.delete("/{id}", response_model=Message)
def delete_user(session: SessionDependency, id: uuid.UUID):
    deleted = user_crud.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")
