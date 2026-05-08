import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.core.security import TokenDependency, hash_password, verify_password
from app.db.database import SessionDependency
from app.models.generic import TokenPayload
from app.models.user import (
    UpdatePassword,
    User,
    UserCreate,
    UserRole,
    UsersPublic,
    UserUpdate,
)


# CRUD operations for User model
# These functions interact with the database to perform create, read, and authentication operations for users.
async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    user = User.model_validate(
        user_create, update={"hashed_password": hash_password(user_create.password)}
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# Read operations for users, including fetching all users, fetching by ID, and fetching by email. These are used in various API endpoints to retrieve user data.
async def get_users(*, session: AsyncSession) -> UsersPublic:
    statement = select(User)
    result = await session.execute(statement)
    users = result.scalars().all()
    return UsersPublic(data=users, count=len(users))


# Fetch a user by ID, which is used for various operations. Returns the user or None if not found.
async def get_user_by_id(*, session: AsyncSession, id: uuid.UUID) -> User | None:
    return await session.get(User, id)


# Fetch a user by email, which is used for authentication. Returns the user or None if not found.
async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


# Update operation for users, allowing updates to the full name, role, and active status. Returns the updated user or None if not found.
async def update_user(
    *, session: AsyncSession, id: uuid.UUID, user_update: UserUpdate
) -> User | None:
    user = await get_user_by_id(session=session, id=id)

    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_data)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


# Delete operation for users, allowing deletion by ID. Returns a boolean indicating success or failure of the deletion.
async def delete_user(*, session: AsyncSession, id: uuid.UUID) -> bool:
    user = await get_user_by_id(session=session, id=id)

    if not user:
        return False

    await session.delete(user)
    await session.commit()

    return True


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


# Authentication function that verifies user credentials. It checks if the user exists and if the provided password matches the stored hashed password. Returns the user if authentication is successful, or None if it fails.
async def authenticate_user(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    else:
        return db_user


# Dependency to get the current authenticated user based on the JWT token. It decodes the token, validates it, and retrieves the user from the database. Raises appropriate HTTP exceptions if validation fails or if the user is not found or inactive.
async def get_current_user(session: SessionDependency, token: TokenDependency) -> User:
    # fmt: off
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
    user = await session.get(User, token_data.sub)
    # fmt: on

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# Role-based access control dependencies (RBAC)
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the necessary permissions.",
            )
        return current_user


# Define access levels
ALLOW_ADMIN = RoleChecker([UserRole.ADMIN])
ALLOW_USER = RoleChecker([UserRole.USER])
ALLOW_ADMIN_AND_USER = RoleChecker([UserRole.ADMIN, UserRole.USER])


# Define a reusable type alias
AllowAdmin = Annotated[User, Depends(ALLOW_ADMIN)]
AllowlUser = Annotated[User, Depends(ALLOW_USER)]
AllowAdminAndUser = Annotated[User, Depends(ALLOW_ADMIN_AND_USER)]


# Type alias for the current authenticated user, used in dependencies for role-based access control. This allows for cleaner code when specifying dependencies that require the current user.
CurrentUser = Annotated[User, Depends(get_current_user)]


# Update operation for changing a user's password, which requires verification of the current password. Returns a success message or raises an HTTP exception if verification fails.
async def update_password(
    *, session: AsyncSession, updatePassword: UpdatePassword, current_user: CurrentUser
) -> bool:

    verified = verify_password(
        updatePassword.current_password, current_user.hashed_password
    )

    if not verified:
        raise HTTPException(status_code=400, detail="Incorrect password")
    if updatePassword.current_password == updatePassword.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )

    hashed_password = hash_password(updatePassword.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    await session.commit()

    return True
