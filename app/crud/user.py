import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.security import TokenDependency, hash_password, verify_password
from app.db.database import SessionDependency
from app.models.generic import TokenPayload
from app.models.user import User, UserCreate, UsersPublic, UserUpdate


# CRUD operations for User model
# These functions interact with the database to perform create, read, and authentication operations for users.
def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(
        user_create, update={"hashed_password": hash_password(user_create.password)}
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Read operations for users, including fetching all users, fetching by ID, and fetching by email. These are used in various API endpoints to retrieve user data.
def get_users(*, session: Session) -> UsersPublic:
    statement = select(User)
    users = session.exec(statement).all()
    return UsersPublic(data=users, count=len(users))


# Fetch a user by ID, which is used for various operations. Returns the user or None if not found.
def get_user_by_id(*, session: Session, id: uuid.UUID) -> User | None:
    statement = select(User).where(User.id == id)
    return session.exec(statement).first()


# Fetch a user by email, which is used for authentication. Returns the user or None if not found.
def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


# Update operation for users, allowing updates to the full name. Returns the updated user or None if not found.
def update_user(
    *, session: Session, id: uuid.UUID, user_update: UserUpdate
) -> User | None:
    user = get_user_by_id(session=session, id=id)

    if not user:
        return None

    user.sqlmodel_update(user_update)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


# Delete operation for users, allowing deletion by ID. Returns a boolean indicating success or failure of the deletion.
def delete_user(*, session: Session, id: uuid.UUID) -> bool:
    user = get_user_by_id(session=session, id=id)

    if not user:
        return False

    session.delete(user)
    session.commit()

    return True


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


# Authentication function that verifies user credentials. It checks if the user exists and if the provided password matches the stored hashed password. Returns the user if authentication is successful, or None if it fails.
def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
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
def get_current_user(session: SessionDependency, token: TokenDependency) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except InvalidTokenError, ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# Type alias for the current authenticated user, used in dependencies for role-based access control. This allows for cleaner code when specifying dependencies that require the current user.
CurrentUser = Annotated[User, Depends(get_current_user)]
