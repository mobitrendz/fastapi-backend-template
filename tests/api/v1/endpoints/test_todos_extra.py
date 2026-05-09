import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import todo as todo_crud
from app.models.todo import ToDoListCreate
from app.models.user import UserCreate, UserRole


@pytest.mark.asyncio
async def test_user_cannot_read_another_users_todo_crud(session: AsyncSession):
    from app.crud import user as user_crud

    # Create user 1 and their todo
    user1_in = UserCreate(
        full_name="User 1",
        email="user1_todo@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user1 = await user_crud.create_user(session=session, user_create=user1_in)
    todo_in = ToDoListCreate(title="User 1 Todo", description="Private")
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_in, current_user=user1
    )

    # Create user 2
    user2_in = UserCreate(
        full_name="User 2",
        email="user2_todo@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user2 = await user_crud.create_user(session=session, user_create=user2_in)

    # User 2 tries to get User 1's todo via CRUD
    fetched_todo = await todo_crud.get_todo_by_id(
        session=session, id=todo.id, current_user=user2
    )
    assert fetched_todo is None


@pytest.mark.asyncio
async def test_admin_can_read_any_users_todo_crud(session: AsyncSession):
    from app.crud import user as user_crud

    # Create user 1 and their todo
    user1_in = UserCreate(
        full_name="User 1",
        email="user1_admin_todo@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user1 = await user_crud.create_user(session=session, user_create=user1_in)
    todo_in = ToDoListCreate(title="User 1 Todo", description="Private")
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_in, current_user=user1
    )

    # Create admin
    admin_in = UserCreate(
        full_name="Admin",
        email="admin_todo@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.ADMIN,
    )
    admin = await user_crud.create_user(session=session, user_create=admin_in)

    # Admin tries to get User 1's todo via CRUD
    fetched_todo = await todo_crud.get_todo_by_id(
        session=session, id=todo.id, current_user=admin
    )
    assert fetched_todo is not None
    assert fetched_todo.id == todo.id


@pytest.mark.asyncio
async def test_update_todo_not_found_crud(session: AsyncSession):
    from app.crud import user as user_crud
    from app.models.todo import ToDoListUpdate

    user_in = UserCreate(
        full_name="User",
        email="todo_notfound@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    update_data = ToDoListUpdate(title="New Title")
    result = await todo_crud.update_todo(
        session=session, id=uuid.uuid4(), todo_update=update_data, current_user=user
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_todo_not_found_crud(session: AsyncSession):
    from app.crud import user as user_crud

    user_in = UserCreate(
        full_name="User",
        email="todo_del_notfound@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    result = await todo_crud.delete_todo(
        session=session, id=uuid.uuid4(), current_user=user
    )
    assert result is False
