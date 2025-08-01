from typing import AsyncGenerator, Generator
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Import settings - handle both direct and Docker environments
try:
    from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB
except ImportError:
    # Fallback to environment variables if settings.py not available
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Admin123")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "practice_fastapi")

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    Handles both local development and Docker environments.
    URL-encodes credentials to handle special characters like @ in passwords.
    Uses psycopg3 for modern PostgreSQL connectivity.
    """
    # URL-encode credentials to handle special characters
    encoded_user = quote_plus(str(POSTGRES_USER))
    encoded_password = quote_plus(str(POSTGRES_PASSWORD))
    
    # If running in Docker, use the Docker service name for the host
    host = "db" if os.environ.get("DOCKER_ENV") else "localhost"
    return f"postgresql+psycopg://{encoded_user}:{encoded_password}@{host}:5432/{POSTGRES_DB}"


# Async engine and session factory
async_engine = create_async_engine(get_database_url())
async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

# Sync engine and session factory
sync_engine = create_engine(get_database_url())
sync_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new async database session.
    """
    async with async_session_factory() as session:
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


def create_sync_session() -> Session:
    """
    Create a synchronous database session for scripts.
    """
    return sync_session_factory()
