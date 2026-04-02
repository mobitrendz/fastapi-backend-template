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