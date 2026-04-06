from app.models.user import UserCreate, UserUpdate, UserRead
from fastapi import APIRouter, HTTPException, Response, status

from app.core.database import SessionDep
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(session: SessionDep, user_create: UserCreate):
    return user_service.create_user(session=session, user_create=user_create)


@router.get("/", response_model=list[UserRead])
def get_users(session: SessionDep):
     return user_service.get_users(session=session)


@router.get("/{id}", response_model=UserRead)
def get_user_by_id(session: SessionDep, id: int):
    return user_service.get_user_by_id(session=session, id=id)


@router.get("/{email}", response_model=UserRead)
def get_user_by_email(session: SessionDep, email: str):
    return user_service.get_user_by_email(session=session, email=email)


@router.patch("/{id}", response_model=UserRead)
def update_user(session: SessionDep, id: int, user_update: UserUpdate):
    return user_service.update_user(session=session, id=id, user_update=user_update)


@router.delete("/{id}")
def delete_user(session: SessionDep, id: int):
    deleted = user_service.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
