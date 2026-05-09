from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi_pagination import add_pagination
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from app.core import security
from app.core.config import settings
from app.crud import user as user_crud
from app.db.database import get_session
from app.main import app
from app.models.user import UserCreate, UserRole

add_pagination(app)


# Testcontainer for Postgres
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:18") as container:
        yield container


@pytest_asyncio.fixture(scope="session")
async def engine(postgres_container):
    # Dynamically build the connection URL from the container
    url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql+psycopg"
    )
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession]:
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def superuser_token(session: AsyncSession) -> str:
    user = await user_crud.get_user_by_email(
        session=session, email=settings.SUPER_USER_EMAIL
    )
    if not user:
        user_in = UserCreate(
            full_name=settings.SUPER_USER_NAME,
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD,
            role=UserRole.SUPER,
        )
        user = await user_crud.create_user(session=session, user_create=user_in)

    return security.create_access_token(str(user.id))


@pytest_asyncio.fixture
async def admin_user_token(session: AsyncSession) -> str:
    email = "admin@example.com"
    user = await user_crud.get_user_by_email(session=session, email=email)
    if not user:
        user_in = UserCreate(
            full_name="Admin User",
            email=email,
            password="password123",  # noqa: S106
            role=UserRole.ADMIN,
        )
        user = await user_crud.create_user(session=session, user_create=user_in)

    return security.create_access_token(str(user.id))


@pytest_asyncio.fixture
async def normal_user_token(session: AsyncSession) -> str:
    email = "user@example.com"
    user = await user_crud.get_user_by_email(session=session, email=email)
    if not user:
        user_in = UserCreate(
            full_name="Normal User",
            email=email,
            password="password123",  # noqa: S106
            role=UserRole.USER,
        )
        user = await user_crud.create_user(session=session, user_create=user_in)

    return security.create_access_token(str(user.id))
