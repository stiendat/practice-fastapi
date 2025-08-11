from typing import AsyncGenerator
from contextvars import ContextVar
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url.replace("postgresql://", "postgresql+psycopg://")
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"


engine = create_async_engine(get_database_url())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session.
    """
    async with session_factory() as db:
        yield db

db_session_context: ContextVar[AsyncSession] = ContextVar("db_session_context")
