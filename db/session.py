# region Common interaction with database
from typing import Generator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

import settings

engine = create_async_engine(settings.DB_URL, future=True, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> Generator:
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session


# endregion
