import logging

from sqlmodel import create_engine, Session, select

from app.core.config import settings 
from app.models.user import User, UserCreate
from app.services import user_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_url = settings.POSTGRES_URL
engine = create_engine(database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

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
    logger.info("Initial data already present")
    if not user:
        user_in = UserCreate(
            name=settings.SUPER_USER_NAME,
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD,
            is_superuser=True
        )
        user = user_service.create_user(session=session, user_create=user_in)
        logger.info("Initial data created")