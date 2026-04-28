from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.core.security import TokenDependency, oauth2_scheme
from app.crud import user as user_crud
from app.db.database import SessionDependency
from app.models.generic import Token
from app.models.user import UserPublic

router = APIRouter()


# This endpoint allows users to log in and receive an access token for authentication in future requests.
@router.post("/access-token", response_model=Token)
async def login_access_token(
    session: SessionDependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await user_crud.authenticate_user(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=security.create_access_token(
            str(user.id), expires_delta=access_token_expires
        )
    )


# This endpoint allows authenticated users to retrieve their access token.
@router.get("/secure-data")
async def read_secure(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    return {"token": token}


# This endpoint allows authenticated users to retrieve their own user information using the access token.
@router.get("/current-user", response_model=UserPublic)
async def get_current_user(
    session: SessionDependency, token: TokenDependency
) -> UserPublic:
    user = await user_crud.get_current_user(session=session, token=token)
    return UserPublic.model_validate(user)
