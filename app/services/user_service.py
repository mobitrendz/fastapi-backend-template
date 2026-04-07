import uuid
import logging
from typing import List
from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserUpdate
from app.core.security import hash_password

logger = logging.getLogger(__name__)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(user_create, update={"hashed_password": hash_password(user_create.password)})
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_users(*, session: Session) -> List[User]:
    statement = select(User)
    return session.exec(statement).all()  # ty:ignore[invalid-return-type]


def get_user_by_id(*, session: Session, id: uuid.UUID) -> User | None:
    statement = select(User).where(User.id == id)
    return session.exec(statement).first()


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

     
def update_user(*, session: Session, id:uuid.UUID, user_update: UserUpdate) -> User | None:
    user = get_user_by_id(session=session, id=id)
    
    if not user:
        return None

    user.sqlmodel_update(user_update)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def delete_user(*, session: Session, id:uuid.UUID) -> bool:
    user = get_user_by_id(session=session, id=id)
    
    if not user:
        return False

    session.delete(user)
    session.commit()
    
    return True

