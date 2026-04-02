from sqlmodel import create_engine, Session

from app.core.config import settings 

database_url = settings.postgres_url
engine = create_engine(database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session