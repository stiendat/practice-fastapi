from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB

Base = declarative_base()

def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy (async psycopg).
    """
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

# Create async engine & session factory
engine = create_async_engine(get_database_url(), echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new async database session for FastAPI dependency injection.
    """
    async with session_factory() as session:
        yield session
