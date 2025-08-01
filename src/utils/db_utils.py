from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB

Base = declarative_base()

def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    """
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

# Asynchronous engine and session factory
async_engine = create_async_engine(get_database_url(), echo=True)
async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

# Synchronous engine and session factory
sync_engine = create_engine(get_database_url(), echo=True)
sync_session_factory = sessionmaker(bind=sync_engine)

def get_db() -> Generator:
    """
    Provide a synchronous database session.
    """
    db = sync_session_factory()
    try:
        yield db
    finally:
        db.close()

async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.
    """
    async with async_session_factory() as session:
        yield session