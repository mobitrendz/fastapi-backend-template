from fastapi import Depends
from collections.abc import Generator
from typing import Annotated

from sqlmodel import create_engine, Session

from app.core.config import settings 


database_url = settings.POSTGRES_URL
engine = create_engine(database_url, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]        

