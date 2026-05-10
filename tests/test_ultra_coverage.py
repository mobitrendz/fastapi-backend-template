import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func

from app.crud import todo as todo_crud
from app.crud import user as user_crud
from app.models.todo import ToDoListCreate
from app.models.user import UserCreate, UserRole, UserUpdate


@pytest.mark.asyncio
async def test_contract_integrity_openapi(client: AsyncClient):
    """Verifies that the OpenAPI schema exists and has the expected React-ready models."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "UserPublic" in schema["components"]["schemas"]
    assert "ToDoListPublic" in schema["components"]["schemas"]
    assert "Message" in schema["components"]["schemas"]


@pytest.mark.asyncio
async def test_rbac_user_list_forbidden(client: AsyncClient, normal_user_token: str):
    response = await client.get(
        "/api/v1/users/", headers={"Authorization": f"Bearer {normal_user_token}"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_rbac_admin_stats(client: AsyncClient, admin_user_token: str):
    response = await client.get(
        "/api/v1/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rbac_super_logs(client: AsyncClient, superuser_token: str):
    response = await client.get(
        "/api/v1/admin/dashboard/logs",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_registration_full_path(client: AsyncClient):
    """Hits missing lines 77-91 in login.py."""
    email = f"new_{uuid.uuid4().hex[:6]}@example.com"
    response = await client.post(
        "/api/v1/login/signup",
        json={"email": email, "password": "password123", "full_name": "New User"},
    )
    assert response.status_code == 200  # Signup returns 200 in current implementation
    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_user_crud_not_found_branches(session: AsyncSession):
    """Hits missing lines 76, 94 in app/crud/user.py."""
    fake_id = uuid.uuid4()
    assert (
        await user_crud.update_user(
            session=session, id=fake_id, user_update=UserUpdate(full_name="No")
        )
        is None
    )
    assert await user_crud.delete_user(session=session, id=fake_id) is False


@pytest.mark.asyncio
async def test_todo_crud_admin_ownership_branch(session: AsyncSession):
    """Hits missing line 65 in app/crud/todo.py (Admin accessing regular user todo)."""
    # 1. Create User and Admin
    user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(
            email=f"u_{uuid.uuid4().hex[:4]}@example.com",
            password="password",
            full_name="User",
        ),
    )
    admin = await user_crud.create_user(
        session=session,
        user_create=UserCreate(
            email=f"a_{uuid.uuid4().hex[:4]}@example.com",
            password="password",
            full_name="Admin",
            role=UserRole.ADMIN,
        ),
    )

    # 2. Create Todo for User
    todo = await todo_crud.create_todo(
        session=session, todo_create=ToDoListCreate(title="T"), current_user=user
    )

    # 3. Admin should be able to get it (This hits the logic in get_todo_by_id)
    fetched = await todo_crud.get_todo_by_id(
        session=session, id=todo.id, current_user=admin
    )
    assert fetched is not None
    assert fetched.id == todo.id


@pytest.mark.asyncio
async def test_seeder_idempotency(session: AsyncSession):
    """Verifies seeding logic doesn't fail on second run."""
    from app.db.initial_data import init

    await init()  # Run seeder
    # Check superuser count
    from sqlmodel import select

    from app.models.user import User, UserRole

    res = await session.execute(
        select(func.count()).select_from(User).where(User.role == UserRole.SUPER)
    )
    count = res.scalar()
    assert count is not None
    assert count >= 1

    # Run again - should not raise exception
    await init()
