from sqlmodel import Session, select

from app.core.config import settings
from app.models.user import User, SuperUserCreate
from app.crud import user as user_crud
from app.db.database import engine

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:    
    init()
    

# if __name__ == "__main__":
#     main()


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    logger.info("Creating initial data")

    user = session.exec(
        select(User).where(User.email == settings.SUPER_USER_EMAIL)
    ).first()
    
    if not user:
        user_in = SuperUserCreate(
            full_name=settings.SUPER_USER_NAME,
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD
        )
        user = user_crud.create_super_user(session=session, user_create=user_in)
        logger.info("Initial data created")
    else:
        logger.info("Initial data already present")

