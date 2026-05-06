import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserCreate, UserRole, UserUpdate

@pytest.mark.asyncio
async def test_update_password_success(client: AsyncClient, normal_user_token: str):
    response = await client.patch(
        "/api/v1/users/password",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"current_password": "password123", "new_password": "newpassword123"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

@pytest.mark.asyncio
async def test_update_password_incorrect_current(client: AsyncClient, normal_user_token: str):
    response = await client.patch(
        "/api/v1/users/password",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"current_password": "wrongpassword", "new_password": "newpassword123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect password"

@pytest.mark.asyncio
async def test_update_password_same_as_current(client: AsyncClient, session: AsyncSession, mocker):
    from app.crud import user as user_crud
    from app.core import security
    
    # Create a fresh user for this test to avoid session issues
    email = f"samepass_{uuid.uuid4().hex[:6]}@example.com"
    user_in = UserCreate(
        full_name="Same Pass",
        email=email,
        password="password123",
        role=UserRole.USER
    )
    user = await user_crud.create_user(session=session, user_create=user_in)
    token = security.create_access_token(str(user.id))
    
    response = await client.patch(
        "/api/v1/users/password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": "password123", "new_password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "New password cannot be the same as the current one"

@pytest.mark.asyncio
async def test_update_password_failure_mock(client: AsyncClient, normal_user_token: str, mocker):
    mocker.patch("app.api.v1.endpoints.users.user_crud.update_password", return_value=False)
    response = await client.patch(
        "/api/v1/users/password",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"current_password": "password123", "new_password": "newpassword123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Failed to update password"

@pytest.mark.asyncio
async def test_read_user_by_id_forbidden(client: AsyncClient, normal_user_token: str, session: AsyncSession):
    # Create another user
    from app.crud import user as user_crud
    other_user_in = UserCreate(
        full_name="Other User",
        email="other_forbidden@example.com",
        password="password123",
        role=UserRole.USER
    )
    other_user = await user_crud.create_user(session=session, user_create=other_user_in)
    
    response = await client.get(
        f"/api/v1/users/byID/{other_user.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

@pytest.mark.asyncio
async def test_update_user_permissions_denied(client: AsyncClient, normal_user_token: str, session: AsyncSession):
    # Create another user
    from app.crud import user as user_crud
    other_user_in = UserCreate(
        full_name="Other User",
        email=f"other_{uuid.uuid4().hex[:6]}@example.com",
        password="password123",
        role=UserRole.USER
    )
    other_user = await user_crud.create_user(session=session, user_create=other_user_in)
    
    # Try to update other user as normal user
    response = await client.patch(
        f"/api/v1/users/{other_user.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"full_name": "New Name"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_role_denied_for_normal_user(client: AsyncClient, normal_user_token: str, session: AsyncSession):
    from app.crud import user as user_crud
    user = await user_crud.get_user_by_email(session=session, email="user@example.com")
    
    response = await client.patch(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {normal_user_token}"},
        json={"role": UserRole.ADMIN}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_user_success(client: AsyncClient, superuser_token: str, session: AsyncSession):
    from app.crud import user as user_crud
    user_in = UserCreate(
        full_name="To Delete",
        email=f"todelete_{uuid.uuid4().hex[:6]}@example.com",
        password="password123",
        role=UserRole.USER
    )
    user = await user_crud.create_user(session=session, user_create=user_in)
    
    response = await client.delete(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

@pytest.mark.asyncio
async def test_delete_user_not_found(client: AsyncClient, superuser_token: str):
    random_id = uuid.uuid4()
    response = await client.delete(
        f"/api/v1/users/{random_id}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
