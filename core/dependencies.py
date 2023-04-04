from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import settings
from database.database_session import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    
    try:
        yield session
    finally:
        await session.close()

