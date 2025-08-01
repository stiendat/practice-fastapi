from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    Always use SQLite for simplicity.
    """
    # Always use SQLite for now to avoid connection issues
    db_path = os.path.abspath("library.db")
    return f"sqlite+aiosqlite:///{db_path}"


# Create async engine with SQLite
engine = create_async_engine(get_database_url(), echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session.
    """
    async with session_factory() as session:
        yield session
