import uuid

import pytest
from httpx import AsyncClient


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
