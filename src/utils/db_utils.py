from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    """
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5435/{POSTGRES_DB}"


engine = create_async_engine(get_database_url())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_database_session() -> AsyncSession:
    """
    Create a new database session.
    """
    return session_factory()


async def create_tables():
    """
    Create all tables in the database.
    """
    async with engine.begin() as conn:
        from src.models import Book, User, Rental
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """
    Drop all tables in the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
