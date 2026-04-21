from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
