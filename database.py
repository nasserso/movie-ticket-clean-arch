from sqlalchemy import QueuePool, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession
)

from settings import Settings


engine = create_async_engine(
    Settings().DATABASE_URL,
    # isolation_level="SERIALIZABLE",
    # poolclass=QueuePool,
)

async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
