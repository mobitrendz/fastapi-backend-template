## My FastAPI - A FastAPI learning project
A step by step guide by 
Sreeraj Sreenivasan - 30 Mar 2026

### Create and run a new FastAPI project

- Create a python project using UV (Assuming UV is already installed)

```bash
uv init my-fastapi
cd my-fastapi
```

- Create python virtual environment

```bash
uv venv
```

- Activate virtual environment

```bash
source .venv/bin/activate
```

- To check the active virtual environment

```bash
which python
```

- Install FastAPI dependency

```bash
uv add fastapi --extra standard
```

- Modify main.py 

```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}
```

- Run FastAPI

```bash
uv run fastapi dev
```

### Start creating project folders

- Create folders app, app/api

- Create `__init__.py` file in all the new folders

- Create welcome.py in app/api folder and add

```bash
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["welcome"])

@router.get("/")
def get_welcome_message():
    return {"message": "Welcome User!"}

@router.get("/{user_name}")
def get_welcome_message_user(user_name: str):
    return {"message": "Welcome " + user_name + "!"}
```

- Modify and move main.py to app folder

```bash
from fastapi import FastAPI
from app.api import welcome

app = FastAPI()

app.include_router(welcome.router)
```

### Adding log support 

- Modified main.py with FastAPI default logging mechanism

```bash
import logging

from fastapi import FastAPI
from app.api import welcome

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    logger.info("FastAPI starting...")

app.include_router(welcome.router)

@app.on_event("shutdown")
def on_shutdown():
    logger.info("FastAPI stopping...")
```

### Adding pytest

- Make sure virtual environment is active before installing pytest 

```bash
uv add pytest --dev
```

- Create folders tests, tests/api in the root folder

- Create `__init__.py` file in all the new folders

- Create test_welcome.py in test/api and add testing code

```bash
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_welcome_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome User!"}

def test_get_welcome_message_user():
    response = client.get("/Sreeraj")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Sreeraj!"}
```

- Run test

```bash
pytest
```

### Adding pytest coverage

```bash
uv add --dev pytest-cov
```

- Run test with coverage

- Basic coverage

```bash
uv run pytest --cov=tests
```

- Detailed report

```bash
uv run pytest --cov=tests --cov-report=term-missing
```

- Permanent configuration
- To avoid typing --cov every time, add the following to pyproject.toml

```bash
[tool.pytest.ini_options]
addopts = "--cov=tests --cov-report=term-missing"
```

- Ignore the deprecated warning as it is backward compatible. Now coverage will run with pytest command

### Adding .env environment variables settings file

- Install dependencies - We need pydantic settings package to enable .env file support.

```bash
uv add pydantic-settings
```

- Create .env file in the project root folder and add

```bash
# Environment: local, staging, production
ENVIRONMENT=local
```

- Create folder named core inside app folder

- Add `__init__.py` file whenever a new folder is created for .py files

- Create config.py inside core folder and add

```bash
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # ty:ignore[missing-argument]
```

- Modify welcome.py 

```bash
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="", tags=["welcome"])

@router.get("/getEnvironment")
def get_env_settings():
    return {"Environment": settings.environment}

@router.get("/{user_name}")
def get_welcome_message_user(user_name: str):
    return {"message": "Welcome " + user_name + "!"}

@router.get("/")
def get_welcome_message():
    return {"message": "Welcome User!"}
```

- Run fastapi

```bash
uv run fastapi dev
```

- Open a browser and enter URL

```bash
http://127.0.0.1:8000/getEnvironment
```

- Expected result is: {"Environment":"local"}

### Adding Postgres DB connection using SQLModel 

- Install PostgreSQL and create a database named my_fastapi

- Install SQLModel dependencies

```bash
uv add sqlmodel psycopg2-binary
```

- Modify .evn file,  add 

```bash
POSTGRES_URL="postgresql://postgres:admin@localhost:5432/my_fastapi"
```

- Update config.py by adding “postgres_url: str”

```bash
class Settings(BaseSettings):
    environment: str
    postgres_url: str
```

- Create database.py file in core folder and add

```bash
from sqlmodel import create_engine, Session

from app.core.config import settings 

database_url = settings.postgres_url
engine = create_engine(database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

- Update welcome.py by adding one more function to check database connection

```bash
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, text

from app.core.config import settings
from app.core.database import get_session

router = APIRouter(prefix="", tags=["welcome"])

@router.get("/checkDBConnection")
def check_database_connection(session: Session = Depends(get_session)):
    try:
        session.exec(text("SELECT 1"))  # ty:ignore[no-matching-overload]
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}") 
```

- Restart the server and check

```bash
http://127.0.0.1:8000/checkDBConnection
```

- Expected output on connection success

```bash
{"status":"ok","database":"connected"}
```

- Expected output on connection fail (modify POSTGRES_URL in .env file with wrong values)

```bash
{"detail":"Database connection failed: (psycopg2.OperationalError) connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  database \"my_fastap\" does not exist\n\n(Background on this error at: https://sqlalche.me/e/20/e3q8)"}
```

### Creating database table using Alembic

- Install Alembic dependency

```bash
uv add alembic
```

- Initialize Alembic

```bash
uv run alembic init migrations
```

- Create folder named models in the app folder

- Create user.py inside app/models folder and add

```bash
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    name: str
    email: str
    password: str

class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class UserCreate(UserBase):
    pass
```

- Import SQLModel in migrations/script.py.mako

```bash
from alembic import op
import sqlalchemy as sa
import sqlmodel
```

- Import SQLModel, User in migrations/env.py

```bash
from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

from app.models.user import User
```

- Update target_metadata in  migrations/env.py

```bash
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata
```

- Update sqlalchemy.url in alembic.ini

```bash
# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = postgresql://postgres:admin@localhost:5432/my_fastapi
```

- Run alembic revision 

```bash
uv run alembic revision --autogenerate -m "create user"
```

- Apply migration

```bash
uv run alembic upgrade head
```

- Expected output

```bash
user table will be created in postgreSQL my_fastapi database.
```

### Adding first super user details to user table on startup

- Add tenacity dependencies 

```bash
uv add tenacity
```

- Add super user details in .env settings file

```bash
SUPER_USER_NAME="Sreeraj Sreenivasan"
SUPER_USER_EMAIL="sreerajs@hotmail.com"
SUPER_USER_PASSWORD="admin"
```

- Update config.py by adding super user variables

```bash
SUPER_USER_NAME: str
SUPER_USER_EMAIL: str
SUPER_USER_PASSWORD: str
```

- Create folder named services inside app folder

- Create user_service.py in app/services folder and add

```bash
from sqlmodel import Session

from app.models.user import User, UserCreate

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(user_create)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user
```

- Update app/core/database.py

```bash
from sqlmodel import create_engine, Session, select

from app.core.config import settings 
from app.models.user import User, UserCreate
from app.services import user_service

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

    user = session.exec(
        select(User).where(User.email == settings.SUPER_USER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            name=settings.SUPER_USER_NAME,
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD,
            is_superuser=True
        )
        user = user_service.create_user(session=session, user_create=user_in)
```

- Create file backend_pre_start.py inside app folder and add

```bash
import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
```

- Create file initial_data.py inside app folder and add

```bash
import logging

from sqlmodel import Session
from app.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    with Session(engine) as session:
        init_db(session)

def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
```

- Create folder named scripts in the project root folder

- Create prestart.sh in scripts folder

```bash
#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py
```

- Modify main.py to call backend_pre_start, initial_data on application startup(instead of running the above shell script, will configure the shell script later in docker compose)

```bash
from app import initial_data, backend_pre_start

@app.on_event("startup")
def on_startup():
    logger.info("FastAPI starting...")
    backend_pre_start.main()
    initial_data.main()
```

- Run the application and check the user table for super user details

### Creating CRUD api endpoints for User

- Update app.models.user.py

```bash
from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    email: str    
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    password: str
```

- Update app.services.user_service.py

```bash
import logging
from typing import List
from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(user_create)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_users(*, session: Session) -> List[User]:
    statement = select(User)
    return session.exec(statement).all()  # ty:ignore[invalid-return-type]


def get_user_by_id(*, session: Session, id: int) -> User | None:
    statement = select(User).where(User.id == id)
    return session.exec(statement).first()


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

     
def update_user(*, session: Session, id:int, user_update: UserUpdate) -> User | None:
    user = get_user_by_id(session=session, id=id)
    
    if not user:
        return None

    user.sqlmodel_update(user_update)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def delete_user(*, session: Session, id:int) -> bool:
    user = get_user_by_id(session=session, id=id)
    
    if not user:
        return False

    session.delete(user)
    session.commit()
    
    return True
```

- Create a file users.py inside app/api folder and add

```bash
from app.models.user import UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException, Response, status

from app.core.database import SessionDep
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(session: SessionDep, user_create: UserCreate):
    return user_service.create_user(session=session, user_create=user_create)


@router.get("/")
def get_users(session: SessionDep):
    return user_service.get_users(session=session)


@router.get("/{id}")
def get_user_by_id(session: SessionDep, id: int):
    return user_service.get_user_by_id(session=session, id=id)


@router.get("/{email}")
def get_user_by_email(session: SessionDep, email: str):
    return user_service.get_user_by_email(session=session, email=email)


@router.patch("/{id}")
def update_user(session: SessionDep, id: int, user_update: UserUpdate):
    return user_service.update_user(session=session, id=id, user_update=user_update)


@router.delete("/{id}")
def delete_user(session: SessionDep, id: int):
    deleted = user_service.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

- Add include router in main.py

```bash
app.include_router(welcome.router)
app.include_router(users.router)
```

- Modify api/core/database.py - SessionDep added

```bash
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
```

- Moved init_db from api/core/database.py to app/initial_data.py(Refer source code)