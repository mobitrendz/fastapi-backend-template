import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=102400,
    parallelism=8,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hash a password using Argon2 with a random salt."""
    if not password:
        raise ValueError("Password must not be empty")

    return pwd_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Validate a plaintext password against an Argon2 hash."""
    try:
        return pwd_hasher.verify(hashed_password, password)
    except Argon2Error:
        return False


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token for a subject (typically a user id or email)."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.utcnow()
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate a JWT access token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
