import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.crud import todo as todo_crud
from app.crud import user as user_crud
from app.models.todo import ToDoListCreate
from app.models.user import UserCreate, UserRole


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient, normal_user_token: str):
    response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={
            "title": "Draft project checklist",
            "description": "Break down the implementation work",
            "status": "pending",
            "due_date_time": "2026-05-10T09:30:00Z",
            "priority": "high",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Draft project checklist"
    assert data["description"] == "Break down the implementation work"
    assert data["status"] == "pending"
    assert data["priority"] == "high"
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_read_todos_returns_current_users_todos_only(
    client: AsyncClient, session: AsyncSession, normal_user_token: str
):
    owner = await user_crud.get_user_by_email(session=session, email="user@example.com")
    assert owner is not None

    other_user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(
            full_name="Other User",
            email="other_todo_user@example.com",
            password="password123",  # noqa: S106
            role=UserRole.USER,
        ),
    )
    await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Visible todo"),
        current_user=owner,
    )
    await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Hidden todo"),
        current_user=other_user,
    )

    response = await client.get(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    titles = {todo["title"] for todo in data["data"]}
    assert "Visible todo" in titles
    assert "Hidden todo" not in titles


@pytest.mark.asyncio
async def test_rbac_todo_access(
    client: AsyncClient,
    session: AsyncSession,
    normal_user_token: str,
    admin_user_token: str,
    superuser_token: str,
):
    # 1. Create a SUPER user todo
    super_user = await user_crud.get_user_by_email(
        session=session, email=settings.SUPER_USER_EMAIL
    )
    assert super_user is not None
    super_todo = await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Super secret todo"),
        current_user=super_user,
    )

    # 2. Create a normal USER todo
    user = await user_crud.get_user_by_email(session=session, email="user@example.com")
    assert user is not None
    await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "User todo"},
    )

    # --- Test SUPER Access ---
    # SUPER should see both
    super_response = await client.get(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert super_response.status_code == 200
    super_titles = {t["title"] for t in super_response.json()["data"]}
    assert "Super secret todo" in super_titles
    assert "User todo" in super_titles

    # --- Test ADMIN Access ---
    # ADMIN should see User todo but NOT Super todo
    admin_response = await client.get(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert admin_response.status_code == 200
    admin_titles = {t["title"] for t in admin_response.json()["data"]}
    assert "User todo" in admin_titles
    assert "Super secret todo" not in admin_titles

    # ADMIN should get 404/403 (effectively 404 in our impl) for Super todo specifically
    admin_single_response = await client.get(
        f"/api/v1/todos/{super_todo.id}",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert admin_single_response.status_code == 404

    # --- Test USER Access ---
    # USER should NOT see Super todo
    user_single_response = await client.get(
        f"/api/v1/todos/{super_todo.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert user_single_response.status_code == 404


@pytest.mark.asyncio
async def test_read_update_and_delete_todo(client: AsyncClient, normal_user_token: str):
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Ship todos", "priority": "medium"},
    )
    todo_id = create_response.json()["id"]

    read_response = await client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert read_response.status_code == 200
    assert read_response.json()["id"] == todo_id

    update_response = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"status": "in progress", "priority": "high"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "in progress"
    assert update_response.json()["priority"] == "high"

    delete_response = await client.delete(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "ToDo deleted successfully"

    read_deleted_response = await client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert read_deleted_response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_read_another_users_todo(
    client: AsyncClient, session: AsyncSession
):
    first_user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(
            full_name="First User",
            email="first_todo_user@example.com",
            password="password123",  # noqa: S106
            role=UserRole.USER,
        ),
    )
    second_user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(
            full_name="Second User",
            email="second_todo_user@example.com",
            password="password123",  # noqa: S106
            role=UserRole.USER,
        ),
    )
    todo = await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Private todo"),
        current_user=first_user,
    )
    second_user_token = security.create_access_token(str(second_user.id))

    response = await client.get(
        f"/api/v1/todos/{todo.id}",
        headers={"Authorization": f"Bearer {second_user_token}"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo_not_found(client: AsyncClient, normal_user_token: str):
    response = await client.patch(
        f"/api/v1/todos/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Nope"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo_not_found(client: AsyncClient, normal_user_token: str):
    response = await client.delete(
        f"/api/v1/todos/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )

    assert response.status_code == 404
