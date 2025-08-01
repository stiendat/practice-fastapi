from typing import AsyncGenerator
from sqlalchemy import create_engine  
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy (synchronous).
    """
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_async_database_url() -> str:
    """
    Construct the async database URL for SQLAlchemy.
    """
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Sync database for simple operations
sync_engine = create_engine(get_database_url())
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Async database for complex operations  
engine = create_async_engine(get_async_database_url())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

# Sync database dependency
def get_database():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session.
    """
    async with session_factory() as session:
        yield session
