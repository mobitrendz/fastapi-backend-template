import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as user_crud
from app.models.user import UserCreate, UserRole, UserUpdate


@pytest.mark.asyncio
async def test_authenticate_user_success_crud(session: AsyncSession):
    email = "auth_success@example.com"
    user_in = UserCreate(
        full_name="Auth Success",
        email=email,
        password="correctpassword",  # noqa: S106
        role=UserRole.USER,
    )
    await user_crud.create_user(session=session, user_create=user_in)

    user = await user_crud.authenticate_user(
        session=session, email=email, password="correctpassword"
    )  # noqa: S106
    assert user is not None
    assert user.email == email


@pytest.mark.asyncio
async def test_update_user_not_found_coverage(session: AsyncSession):
    result = await user_crud.update_user(
        session=session, id=uuid.uuid4(), user_update=UserUpdate(full_name="No One")
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_user_not_found_coverage(session: AsyncSession):
    result = await user_crud.delete_user(session=session, id=uuid.uuid4())
    assert result is False


@pytest.mark.asyncio
async def test_role_checker_success(session: AsyncSession):
    user_in = UserCreate(
        full_name="Admin User",
        email="admin_check@example.com",
        password="password123",  # noqa: S106
        role=UserRole.ADMIN,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    checker = user_crud.ALLOW_ADMIN
    result = checker(current_user=user)
    assert result == user
