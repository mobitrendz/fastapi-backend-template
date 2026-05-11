import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserCreate


@pytest.mark.asyncio
async def test_create_todo_success(client: AsyncClient, normal_user_token: str):
    response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Test Todo", "description": "Test Description"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"


@pytest.mark.asyncio
async def test_read_todos_coverage(client: AsyncClient, normal_user_token: str):
    response = await client.get(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 200
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_read_todo_by_id_success(client: AsyncClient, normal_user_token: str):
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Find Me", "description": "Found"},
    )
    todo_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == todo_id


@pytest.mark.asyncio
async def test_read_todo_by_id_not_found(client: AsyncClient, normal_user_token: str):
    response = await client.get(
        f"/api/v1/todos/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo_success(client: AsyncClient, normal_user_token: str):
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "To Update", "description": "Old"},
    )
    todo_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Updated"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


@pytest.mark.asyncio
async def test_update_todo_not_found(client: AsyncClient, normal_user_token: str):
    response = await client.patch(
        f"/api/v1/todos/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "New Title"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo_success(client: AsyncClient, normal_user_token: str):
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "To Delete", "description": "Bye"},
    )
    todo_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_todo_not_found(client: AsyncClient, normal_user_token: str):
    response = await client.delete(
        f"/api/v1/todos/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_todo_rbac_admin_access(
    client: AsyncClient, admin_user_token: str, normal_user_token: str
):
    # 1. Create a todo as normal user
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "User Todo", "description": "Private?"},
    )
    todo_id = create_response.json()["id"]

    # 2. Admin should be able to read it
    response = await client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "User Todo"


@pytest.mark.asyncio
async def test_todo_rbac_super_access(
    client: AsyncClient, superuser_token: str, normal_user_token: str
):
    # 1. Create a todo as normal user
    create_response = await client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Secret Todo", "description": "Top Secret"},
    )
    todo_id = create_response.json()["id"]

    # 2. Super should be able to read it
    response = await client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Secret Todo"


@pytest.mark.asyncio
async def test_todo_list_admin(client: AsyncClient, admin_user_token: str):
    response = await client.get(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {admin_user_token}"},
    )
    assert response.status_code == 200
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_read_other_user_todo_forbidden(
    client: AsyncClient, normal_user_token: str, session: AsyncSession
):
    from app.crud import todo as todo_crud
    from app.crud import user as user_crud
    from app.models.todo import ToDoListCreate

    # 1. Create a second user
    email = f"other_todo_{uuid.uuid4().hex[:8]}@example.com"
    other_user_in = UserCreate(
        email=email,
        password="password123",
        full_name="Other Todo User",
    )
    other_user = await user_crud.create_user(session=session, user_create=other_user_in)

    # 2. Create a todo for that second user
    todo_in = ToDoListCreate(title="Other User Todo", description="Private")
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_in, current_user=other_user
    )

    # 3. First user tries to read second user's todo
    response = await client.get(
        f"/api/v1/todos/{todo.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 404  # get_todo_by_id returns None, which raises 404


@pytest.mark.asyncio
async def test_update_other_user_todo_forbidden(
    client: AsyncClient, normal_user_token: str, session: AsyncSession
):
    from app.crud import todo as todo_crud
    from app.crud import user as user_crud
    from app.models.todo import ToDoListCreate

    # 1. Create a second user and their todo
    email = f"other_todo_upd_{uuid.uuid4().hex[:8]}@example.com"
    other_user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(email=email, password="password123", full_name="Other"),
    )
    todo = await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Other Todo", description="Old"),
        current_user=other_user,
    )

    # 2. First user tries to update second user's todo
    response = await client.patch(
        f"/api/v1/todos/{todo.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"title": "Hack"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_user_todo_forbidden(
    client: AsyncClient, normal_user_token: str, session: AsyncSession
):
    from app.crud import todo as todo_crud
    from app.crud import user as user_crud
    from app.models.todo import ToDoListCreate

    # 1. Create a second user and their todo
    email = f"other_todo_del_{uuid.uuid4().hex[:8]}@example.com"
    other_user = await user_crud.create_user(
        session=session,
        user_create=UserCreate(email=email, password="password123", full_name="Other"),
    )
    todo = await todo_crud.create_todo(
        session=session,
        todo_create=ToDoListCreate(title="Other Todo", description="Old"),
        current_user=other_user,
    )

    # 2. First user tries to delete second user's todo
    response = await client.delete(
        f"/api/v1/todos/{todo.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 404
