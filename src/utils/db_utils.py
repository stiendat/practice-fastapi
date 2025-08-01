from typing import AsyncGenerator, Generator
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB
from sqlalchemy import create_engine

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    """
    return os.environ.get("DATABASE_URL", f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}")

# Async engine and session factory
async_engine = create_async_engine(get_database_url())
async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
 
# Sync engine and session factory
sync_engine = create_engine(get_database_url())
sync_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """s
    Create a new database session.
    """
    async with sync_session_factory() as session:
        yield session

def get_db() -> Generator[Session, None, None]:
    """
    Create a new sync database session for dependency injection.
    """
    db = sync_session_factory()
    try:
        yield db
    finally:
        db.close()