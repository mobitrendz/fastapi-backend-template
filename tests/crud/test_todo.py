import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import todo as todo_crud
from app.crud import user as user_crud
from app.models.todo import ToDoListCreate, ToDoListUpdate
from app.models.user import UserCreate, UserRole


@pytest.mark.asyncio
async def test_update_todo_crud(session: AsyncSession):
    user_in = UserCreate(
        full_name="Todo Owner",
        email="todo_owner@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    todo_in = ToDoListCreate(title="Original Title")
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_in, current_user=user
    )

    update_data = ToDoListUpdate(title="Updated Title")
    updated_todo = await todo_crud.update_todo(
        session=session, id=todo.id, todo_update=update_data, current_user=user
    )
    assert updated_todo is not None
    assert updated_todo.title == "Updated Title"


@pytest.mark.asyncio
async def test_delete_todo_crud(session: AsyncSession):
    user_in = UserCreate(
        full_name="Todo Owner 2",
        email="todo_owner2@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)

    todo_in = ToDoListCreate(title="To Delete")
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_in, current_user=user
    )

    result = await todo_crud.delete_todo(session=session, id=todo.id, current_user=user)
    assert result is True


@pytest.mark.asyncio
async def test_get_todos_admin_crud(session: AsyncSession):
    # Create a user and their todo
    user_in = UserCreate(
        full_name="User",
        email="user_admin_test@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.USER,
    )
    user = await user_crud.create_user(session=session, user_create=user_in)
    todo_in = ToDoListCreate(title="User Todo")
    await todo_crud.create_todo(session=session, todo_create=todo_in, current_user=user)

    # Create admin
    admin_in = UserCreate(
        full_name="Admin",
        email="admin_todo_test@example.com",
        password="password123",  # noqa: S106,
        role=UserRole.ADMIN,
    )
    admin = await user_crud.create_user(session=session, user_create=admin_in)

    # Admin should see all todos
    todos = await todo_crud.get_todos(session=session, current_user=admin)
    assert todos.count >= 1
