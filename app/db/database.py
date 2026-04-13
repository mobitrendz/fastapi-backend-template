from fastapi import Depends
from collections.abc import Generator
from typing import Annotated

from sqlmodel import create_engine, Session

from app.core.config import settings 

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]

