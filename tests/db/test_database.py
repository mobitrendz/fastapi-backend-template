import pytest
from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_session():
    async for session in get_session():
        assert isinstance(session, AsyncSession)
