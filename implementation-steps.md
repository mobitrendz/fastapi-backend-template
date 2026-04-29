# FastAPI Backend Template - Step by Step Implementation Details
Developer: Sreeraj Sreenivasan - 30 Mar 2026

### Table of Contents

* [Prerequisites](#Prerequisites)
* [Create and run a new FastAPI project](#Create-and-run-a-new-FastAPI-project)
* [Create Project folders](#Create-Project-folders)
* [Implement log support](#Implement-log-support)
* [Add pytest](#Add-pytest)
* [Add pytest coverage](#Add-pytest-coverage)
* [Create env configuration file](#Create-env-configuration-file)
* [Create PostgreSQL session using SQLModel](#Create-PostgreSQL-session-using-SQLModel)
* [Create database table using Alembic](#Create-database-table-using-Alembic)
* [Add first Super User details to User table on startup](#Add-first-Super-User-details-to-User-table-on-startup)
* [Create CRUD API endpoints for User ](#Create-CRUD-API-endpoints-for-User )
* [ Implement Argon2 Password hashing and UUID](#Implement-Argon2-Password-hashing-and-UUID)
* [Implement OAuth2 JWT Token authentication](#Implement-OAuth2-JWT-Token-authentication)
* [Reorganise project folder structure](#Reorganise-project-folder-structure)
* [Implement Docker](#Implement-Docker)
* [Docker Compose All Apps ](#Docker-Compose-All-Apps)
* [Docker Compose Override for dev env](#Docker-Compose-Override-for-dev-env)
* [Debug App using debugpy](#Debug-App-using-debugpy)
* [Implement FastAPI Lifespan](#Implement-FastAPI-Lifespan)
* [Add Gemini CLI](#Add-Gemini-CLI )
* [Implement Mypy](#Implement-Mypy)
* [Implement Ruff](#Implement-Ruff)
* [Implement Pre-commit](#Implement-Pre-commit)
* [Upgrade from Psycopg2 to Psycopg3 Async](#Upgrade-from-Psycopg2-to-Psycopg3-Async )
* [Implement Role Based Access Control `RBAC`](#Implement-Role-Based-Access-Control-RBAC)
* [Rearrange the order of docker compose](#Rearrange-the-order-of-docker-compose)
* [Implement Zensical](#Implement-Zensical)
* [Implement async](#Implement-async)
* [Implement update password](#Implement-update-password)
* [Implement Email and MailCatcher](#Implement-Email-and-MailCatcher)
* [Replace pre commit with prek](#Replace-pre-commit-with-prek)

### Prerequisites

* Python >=3.14
* PostgreSQL 18
* git
* uv

### Create and run a new FastAPI project

- Create a python project using UV (Assuming UV is already installed)

```bash
uv init fastapi-backend-template
cd fastapi-backend-template
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

### Create Project folders

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

### Implement log support

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

### Add pytest

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

### Add pytest coverage

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

### Create env configuration file

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

### Create PostgreSQL session using SQLModel

- Install PostgreSQL and create a database named my_fastapi

- Install SQLModel dependencies

```bash
uv add sqlmodel "psycopg[binary]"
```

- Modify .evn file,  add

```bash
POSTGRES_URL="postgresql+psycopg://postgres+:admin@localhost:5432/my_fastapi"
```

- Update config.py by adding POSTGRES_URL: str”

```bash
class Settings(BaseSettings):
    ENVIRONMENT: str
    POSTGRES_URL: str
```

- Create database.py file in core folder and add

```bash
from sqlmodel import create_engine, Session

from app.core.config import settings

database_url = settings.POSTGRES_URL
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
from app.db.database import get_session

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
{"detail":"Database connection failed: (psycopg3.OperationalError) connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  database \"my_fastap\" does not exist\n\n(Background on this error at: https://sqlalche.me/e/20/e3q8)"}
```

### Create database table using Alembic

- Install Alembic dependency

```bash
uv add alembic
```

- Initialize Alembic

```bash
uv run alembic init alembic
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

- Import SQLModel in alembic/script.py.mako

```bash
from alembic import op
import sqlalchemy as sa
import sqlmodel
```

- Import SQLModel, User in alembic/env.py

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
sqlalchemy.url = postgresql+psycopg://postgres:admin@localhost:5432/my_fastapi
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
user table will get created in postgreSQL my_fastapi database.
```

### Add first Super User details to User table on startup

- Add tenacity dependencies

```bash
uv add tenacity
```

- Add super user details in .env settings file

```bash
ADMIN_USER_NAME="Sreeraj Sreenivasan"
ADMIN_USER_EMAIL="sreerajs@hotmail.com"
ADMIN_USER_PASSWORD="admin"
```

- Update config.py by adding super user variables

```bash
ADMIN_USER_NAME: str
ADMIN_USER_EMAIL: str
ADMIN_USER_PASSWORD: str
```

- Create folders named services, db inside app folder

- Create user.py in app/services folder and add

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
from app.crud import user as user_crud

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
        select(User).where(User.email == settings.ADMIN_USER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            name=settings.ADMIN_USER_NAME,
            email=settings.ADMIN_USER_EMAIL,
            password=settings.ADMIN_USER_PASSWORD,
            is_superuser=True
        )
        user = user.create_user(session=session, user_create=user_in)
```

- Create file backend_pre_start.py inside app/db folder and add

```bash
import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.database import engine

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

- Create file initial_data.py inside app/db folder and add

```bash
import logging

from sqlmodel import Session
from app.db.database import engine, init_db

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
from app.db import initial_data, backend_pre_start

@app.on_event("startup")
def on_startup():
    logger.info("FastAPI starting...")
    backend_pre_start.main()
    initial_data.main()
```

- Run the application and check the user table for super user details

### Create CRUD API endpoints for User

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

- Update app.crud.user.py

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
from fastapi import APIRouter, HTTPException

from app.models.generic import Message
from app.models.user import UserCreate, UserUpdate, UserRead
from app.db.database import SessionDependency
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(session: SessionDependency, user_create: UserCreate):
    return user.create_user(session=session, user_create=user_create)


@router.get("/", response_model=list[UserRead])
def get_users(session: SessionDependency):
     return user.get_users(session=session)


@router.get("/{id}", response_model=UserRead)
def get_user_by_id(session: SessionDependency, id: int):
    return user.get_user_by_id(session=session, id=id)


@router.get("/{email}", response_model=UserRead)
def get_user_by_email(session: SessionDependency, email: str):
    return user.get_user_by_email(session=session, email=email)


@router.patch("/{id}", response_model=UserRead)
def update_user(session: SessionDependency, id: int, user_update: UserUpdate):
    return user.update_user(session=session, id=id, user_update=user_update)


@router.delete("/{id}", response_model=Message)
def delete_user(session: SessionDependency, id: int):
    deleted = user.delete_user(session=session, id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")
```

- Add include router in main.py

```bash
app.include_router(welcome.router)
app.include_router(users.router)
```

- Modify api/core/database.py - SessionDependency added

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

SessionDependency = Annotated[Session, Depends(get_session)]
```

- Create a file `generic.py` inside api/models folder and add

```bash
# Generic message

from sqlmodel import SQLModel

class Message(SQLModel):
    message: str
```

- Moved init_db function from api/core/database.py to app/initial_data.py(Refer source code)

### Implement Argon2 Password hashing and UUID

- Add pwdlib with Argon2 support, jwt dependencies

```bash
uv add "pwdlib[argon2]"
```

- Create security.py in app/core folder and add

```bash
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error

pwd_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=102400,
    parallelism=8,
    hash_len=32,
    salt_len=16,
)

def hash_password(password: str) -> str:
    """Hash a password using Argon2 with a random salt."""
    if not password:
        raise ValueError("Password must not be empty")

    return pwd_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Validate a plaintext password against an Argon2 hash."""
    try:
        return pwd_hasher.verify(hashed_password, password)
    except Argon2Error:
        return False
```

- Modify app/models/user.py

```bash
import uuid
from pydantic import EmailStr
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime

def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime | None
```

- Modify create_user function in user.py

```bash
from app.core.security import hash_password

def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(user_create, update={"hashed_password": hash_password(user_create.password)})

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
```

- Run alembic revision and upgrade to make all the model changes to reflect in the database.

```bash
uv run alembic revision --autogenerate -m “modify user table”
uv run alembic upgrade head
```

- As we modified the user table structure completely, I got some errors while alembic migration and I removed the alembic(alembic folder, alembic.ini file) from the project and dropped alembic_version and user table manually and repeated the alembic initialization steps again.

```bash
uv run alembic init alembic
```

- Import SQLModel in alembic/script.py.mako

```bash
from alembic import op
import sqlalchemy as sa
import sqlmodel
```

- Import SQLModel, User in alembic/env.py

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
sqlalchemy.url = postgresql+psycopg://postgres:admin@localhost:5432/my_fastapi
```

- Run alembic revision and apply migration

```bash
uv run alembic revision --autogenerate -m "create user"
uv run alembic upgrade head
```

- Expected output

```bash
New user table will be created in postgreSQL my_fastapi database.
```

- Restart server and check for the new user data with hashed_password

```bash
uv run fastapi dev
```

### Implement OAuth2 JWT Token authentication

- Add JWT dependencies

```bash
uv add pyjwt
```

- Update .evn file

```bash
# Secret key for JWT token generation
SECRET_KEY=ZBkomvC1HvBIXCrZOSMdub3yRkFDfZOhzSj43r91co8
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- Update app.core.config.py

```bash
SECRET_KEY: str
ALGORITHM: str
ACCESS_TOKEN_EXPIRE_MINUTES: int
```

- Update app/core/security.py with below lines

```bash
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=102400,
    parallelism=8,
    hash_len=32,
    salt_len=16,
)

def hash_password(password: str) -> str:
    """Hash a password using Argon2 with a random salt."""
    if not password:
        raise ValueError("Password must not be empty")

    return pwd_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Validate a plaintext password against an Argon2 hash."""
    try:
        return pwd_hasher.verify(hashed_password, password)
    except Argon2Error:
        return False

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token for a subject (typically a user id or email)."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.utcnow()  # ty:ignore[deprecated]
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate a JWT access token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
```

- Update app.core.generic.py add below lines

```bash
# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
```

- Update app/crud/user.py

```bash
# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"

def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    else:
        return db_user
```

- Create file login.py in app/api folder and add

```bash
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import SessionDependency
from app.core import security
from app.core.config import settings
from  app.crud.user import authenticate_user
from app.models.generic import Token

router = APIRouter(prefix="/login", tags=["Login"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")

@router.post("/access-token", response_model=Token)
def login_access_token(session: SessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = authenticate_user(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(access_token=security.create_access_token(str(user.id), expires_delta=access_token_expires))

@router.get("/secure-data")
def read_secure(token: str = Depends(oauth2_scheme)):
    # This endpoint will show a lock icon in Swagger
    return {"token": token}
```

- Update app/main.py

```bash
app.include_router(welcome.router)
app.include_router(users.router)
app.include_router(login.router)
```

### Reorganise project folder structure

```
fastapi-backend-template/
├── .vscode/                       # Debugging env configuration(launch.json)
├── app/                           # Main Application Logic
│   ├── api/                       # API Entry points
│   │   └── v1/                    # API Versioning
│   │       ├── endpoints/         # Individual route handlers (e.g., users.py)
│   │       └── router.py          # Main router merging all v1 endpoints
│   ├── core/                      # Global configuration and security (JWT, Auth)
│   ├── crud/                      # Reusable database CRUD operations
│   ├── db/                        # Connection engine, session, and seed data
│   ├── models/                    # SQLModels, Tables, and DTOs (Data Transfer Objects)
│   ├── services/                  # Complex business logic and external integrations
│   └── main.py                    # FastAPI application initialization
├── alembic/                       # Database migrations and environment setup
├── scripts/                       # Shell scripts for deployment and startup
├── tests/                         # Pytest suite for unit and integration testing
├── .env                           # Environment variables (Internal)
├── .env.example                   # Template for environment variables
├── alembic.ini                    # Alembic configuration
├── docker-compose.override.yml    # Container Orchestration Manifest for dev env with hot reload
├── docker-compose.yaml            # Container Orchestration Manifest
├── Dockerfile                     # Multi-stage, non-root Production Build
├── pyproject.toml                 # Dependency management (uv/pip)
├── pytest.ini                     # Pytest configuration
└── README.md                      # Project documentation
```

### Implement Docker

**Implementing docker to run only this fastapi project(no database or other apps)**

**1, Modify .env (as PostgreSQL is running on different docker container in my local machine)**
```bash
# Postgres
POSTGRES_SERVER=host.docker.internal
```

**2, Create a file named `Dockerfile` in the root folder and add the below line**
```bash
# 1. Use official python 3.14 (or slim) image
FROM python:3.14-slim-bookworm

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Setup environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 4. Install dependencies
# Using --mount=type=cache speeds up builds by caching uv packages
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 5. Copy application and .env
COPY . .

# 6. Install project itself (if package mode is enabled)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 7. Add .venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# 8. Run Alembic and Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

**3, Create a file named `.dockerignore` in the root folder and add the below line**
```bash
.venv
.git
__pycache__
.env
*.pyc
```

**4, Build Docker Image**
``bash
docker build -t fastapi-backend-template .
```

**4, Run Docker Image**
``bash
docker run -p 8000:8000 --env-file .env fastapi-backend-template
```

**5, Test swagger on browser**
```bash
http://127.0.0.1:8000/docs
```

### Docker Compose All Apps

**Docker Compose FastApi, PostgreSQL, pgAdmin and seeder**

**1, Update Dockerfile**
```bash
# Stage 1: Build dependencies
FROM python:3.14-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

# Stage 2: Runtime
FROM python:3.14-slim-bookworm

WORKDIR /app

# Install curl for the health check and libpq for Postgres compatibility
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq5 && rm -rf /var/lib/apt/lists/*

# Set environment paths
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy virtual env from builder
COPY --from=builder /app/.venv /app/.venv

# Copy project files
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY scripts/ ./scripts/
COPY alembic.ini .env ./

# Ensure the script is executable
RUN chmod +x /app/scripts/prestart.sh

# Default command starts the API
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
```

**2, Create docker-compose.yaml in the root folder and add**

```bash
services:
  db:
    image: postgres:18
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-admin}
      POSTGRES_DB: ${POSTGRES_DB:-fastapi_backend_template}
      # FORCE Postgres to use the mounted path
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d fastapi_backend_template"]
      interval: 3s
      timeout: 3s
      retries: 5

  api:
    build: .
    container_name: fastapi_api
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment: &api_env
      - PYTHONPATH=/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      # Requires a @app.get("/health") route in your FastAPI main.py
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 5s
      timeout: 5s
      retries: 5

  seeder:
    build: .
    container_name: fastapi_seeder
    # Absolute path to the script in the container
    entrypoint: ["/app/scripts/prestart.sh"]
    env_file:
      - .env
    environment: *api_env
    depends_on:
      api:
        condition: service_healthy

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin_ui
    env_file:
      - .env
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
```

**3, Modify scripts/prestart.sh**

```bash
#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/db/backend_pre_start.py

echo "--- RUNNING MIGRATIONS ---"
alembic upgrade head

# Create initial data in DB
python app/db/initial_data.py
```

**4, Update app/main.py**
```bash
@app.get("/health", tags=["Health Check"])
async def health():
    return {"status": "ok"}
```

**5, Update .env file**
```bash
# pgAdmin settings
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## Docker Compose Override for dev env

**Create docker-compose.override.yml(dev env settings) in the root folder**
- This will enable **HOT RELOAD** on dev environment
```bash
services:
  api:
    # Enable Hot Reload by mounting local source code
    volumes:
      - ./app:/app/app
      - ./scripts:/app/scripts
      - ./alembic:/app/alembic
    # Override production 'run' with development 'dev'
    command: ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
    environment:
      - WATCHFILES_FORCE_POLLING=true
      - DEBUG=True

  pgadmin:
    # You might only want pgadmin visible during development
    ports:
      - "5050:80"
```

**Restart the server**

```bash
Docker compose up —build
```

## Debug App using debugpy

(Local env only - not in Docker)

**install **debugpy** (the debugger)**
```bash
uv sync

source .venv/bin/activate

uv add debugpy
```

**Create .vscode folder in root and create launch.json inside it**

```bash
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI: Local Debug",
            "type": "debugpy",
            "request": "launch",
            "module": "fastapi",
            "args": [
                "dev",
                "app/main.py",
                "--port",
                "8000"
            ],
            "envFile": "${workspaceFolder}/.env",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "showReturnValue": true
        }
    ]
}
```

## Implement FastApi Lifespan

**Modify app/main.py**

```bash
from app.db.initial_data import init
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("--- SYSTEM STARTUP ---")

    # 1. Run migrations (Optional: see note below)
    # 2. Seed initial data
    try:
        await init()
        print("--- SEEDING COMPLETE ---")
    except Exception as e:
        print(f"Seeding failed: {e}")

    yield  # The app is now running and "healthy"

    # --- SHUTDOWN LOGIC ---
    print("--- SYSTEM SHUTDOWN ---")

app = FastAPI(lifespan=lifespan)
```

## Add Gemini CLI

**Install Gemini globally**
```bash
brew install gemini-cli
```

**Run**
```bash
gemini
```

**Sandbox**

1, restrict the CLI's access strictly to your current project directory
```bash
gemini --sandbox seatbelt
```

## Implement Mypy

## Implement Ruff

## Implement Zensical

- Install dependency
```bash
uv add --dev zensical
```

- Start New Project
```bash
uv run zensical new .
```

- Live Preview
```bash
uv run zensical serve
```

- Build for Deployment
```bash
uv run zensical build
```

- Check for Issues
```bash
uv run zensical --help
```

## Implement Pre-commit

- Install prek dependency
```bash
uv add --dev prek
uv tool install prek --with prek-uv
```

- Link it to your current repository
```bash
uv run prek install
```

- Create .pre-commit-config.yaml file in the root folder and add
```bash
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
        exclude: ^site/
      - id: end-of-file-fixer
        exclude: ^site/
      - id: check-yaml
      - id: check-added-large-files

  # Ruff: Handles both linting and formatting instantly
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.11
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  # Mypy: Using the mirror ensures a clean environment
  # - repo: https://github.com/pre-commit/mirrors-mypy # or your ty hook
  #   rev: v1.20.1
  #   hooks:
  #     - id: mypy
  #       args: ["--config-file", "pyproject.toml"]
  #       # THIS IS THE KEY: Pre-commit needs to 'see' these to resolve imports
  #       additional_dependencies:
  #         - types-pyjwt
  #         - types-passlib
  #         - fastapi
  #         - pydantic-settings
  #         - sqlmodel

  - repo: local
    hooks:
      - id: ty-check
        name: ty check
        entry: uv run ty check
        language: system
        pass_filenames: false
        always_run: true

  # Bandit: Security-focused linting
  - repo: https://github.com/pycqa/bandit
    rev: 1.8.3
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]

  # uv-lock: Ensures your lockfile is always synced with pyproject.toml
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.11.7
    hooks:
      - id: uv-lock

  # Zensical: Build check for the documentation site
  - repo: local
    hooks:
      - id: zensical-check
        name: zensical build check
        entry: uv run zensical build
        language: system
        pass_filenames: false
        always_run: true
```

- Running your first check
```bash
uv run prek run --all-files
```

- For fixing jwt.exceptions(jwt.*) import error
```bash
uv tool install ty@latest
```

**Still the error is showing, update pyproject.toml**
```bash
[tool.ty.environment]
python = ".venv/bin/python"
python-version = "3.14"
# Add this to ensure ty looks in the site-packages where the stubs live
extra-paths = [".venv/lib/python3.14/site-packages"]

[tool.ty.analysis]
# PRO TIP: For FastAPI and PyJWT, "replace-imports-with-any" is often better.
# It ensures that 'ty' doesn't cause cascading errors in your auth/route logic.
replace-imports-with-any = ["jwt.**", "fastapi.**"]
```

**Clear the Cache and run again**
```bash
prek cache clean
uv run prek run --all-files
```

## Upgrade from Psycopg2 to Psycopg3 Async

**Update app/db/database.py**
- Convert database session management to asynchronous using AsyncSession and create_async_engine.
```python
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]
```

**Update app/crud/user.py**
- Convert all user CRUD operations to be asynchronous.
```python
async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    ...
    await session.commit()
    await session.refresh(user)
    return user

async def get_users(*, session: AsyncSession) -> UsersPublic:
    statement = select(User)
    result = await session.execute(statement)
    users = result.all()
    return UsersPublic(data=users, count=len(users))
```

**Update app/api/v1/endpoints/users.py**
- Update all user endpoints to be asynchronous and use await.
```python
@router.post("/", response_model=UserPublic)
async def create_user(session: SessionDependency, allow_admin: AllowAdmin, user_create: UserCreate):
    return await user_crud.create_user(session=session, user_create=user_create)
```

## Implement Role Based Access Control RBAC

**Update app.model.user.py**
- User roles for role-based access control
```bash
class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
```

- Role-based access control dependencies
```bash
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Annotated[User, Depends(user_crud.get_current_user)]) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the necessary permissions."
            )
        return current_user
```

- Define access levels
```bash
ALLOW_ADMIN = RoleChecker([UserRole.ADMIN])
ALLOW_USER = RoleChecker([UserRole.USER])
ALLOW_ADMIN_AND_USER = RoleChecker([UserRole.ADMIN, UserRole.USER])
```

- Define a reusable type alias
```bash
AllowAdmin = Annotated[User, Depends(ALLOW_ADMIN)]
AllowlUser = Annotated[User, Depends(ALLOW_USER)]
AllowAdminAndUser = Annotated[User, Depends(ALLOW_ADMIN_AND_USER)]
```

**Allow role based access to api's by adding `allow_admin: AllowAdmin` in  app.api.v1.endpoints.users.pt endpoints**
```bash
@router.post("/", response_model=UserPublic)
async def create_user(session: SessionDependency, allow_admin: AllowAdmin, user_create: UserCreate):
    return await user_crud.create_user(session=session, user_create=user_create)
```

## Rearrange the order of docker compose

**Modified docker-compose.yaml**
```bash
services:
  db:
    image: postgres:18
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-admin}
      POSTGRES_DB: ${POSTGRES_DB:-fastapi_db}
      # FORCE Postgres to use the mounted path
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d ${POSTGRES_DB:-fastapi_db}"]
      interval: 3s
      timeout: 3s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin_ui
    env_file:
      - .env
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
      PGADMIN_SESSION_EXPIRATION: 720
    ports:
      - "5050:80"
    depends_on:
      - db

  prestart:
    build: .
    container_name: prestart_migrations
    # Absolute path to the script in the container
    entrypoint: ["/app/scripts/prestart.sh"]
    env_file:
      - .env
    environment:
      - PYTHONPATH=/app
      - POSTGRES_SERVER=db
    depends_on:
      db:
        condition: service_healthy
        restart: true

  backend:
    build: .
    container_name: fastapi_api
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - PYTHONPATH=/app
      - POSTGRES_SERVER=db
    depends_on:
      db:
        condition: service_healthy
        restart: true
      prestart:
        condition: service_completed_successfully
    healthcheck:
      # Requires a @app.get("/health") route in your FastAPI main.py
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Implement async

## Implement update password
Updated app/models/user.py, app/crud/user.py, app/api/v1/endpoints/users.py

## Implement Email and MailCatcher

## Replace pre commit with prek
