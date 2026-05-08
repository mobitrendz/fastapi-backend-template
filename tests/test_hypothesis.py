from hypothesis import given
from hypothesis import strategies as st

from app.core import security
from app.models.user import UserCreate, UserRole


# Property-based test for password hashing verification
@given(st.text(min_size=1, max_size=100))
def test_password_hash_verification(password: str) -> None:
    hashed = security.hash_password(password)
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrong_password", hashed)


# Property-based test for user creation validation
@given(
    email=st.emails(),
    full_name=st.text(min_size=1, max_size=50),
    password=st.text(min_size=8, max_size=100),
)
def test_user_create_model_validation(
    email: str, full_name: str, password: str
) -> None:
    user_in = UserCreate(
        email=email,
        full_name=full_name,
        password=password,
        role=UserRole.USER,
    )
    assert user_in.email.lower() == email.lower()
    assert user_in.full_name == full_name
    assert user_in.password == password
