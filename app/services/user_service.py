from sqlmodel import Session

from app.models.user import User, UserCreate

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(user_create)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user