from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT,POSTGRES_HOST  
import os
from sqlalchemy import select

Base = declarative_base()


def get_database_url():
    return os.getenv("DATABASE_URL")  


engine = create_async_engine(get_database_url(), echo=True)

print("DB URL:", get_database_url())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session.
    """
    async with session_factory() as session:
        yield session
