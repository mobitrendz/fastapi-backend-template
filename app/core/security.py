from app.core.backend_pre_start import main
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error

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

