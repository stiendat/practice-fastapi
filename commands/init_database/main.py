from src.models.sample_models import *
from src.models.todo import Todo
from src.utils.db_utils import Base, get_database_url

from sqlalchemy import create_engine
import asyncio


async def init_database():
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


def main():
    asyncio.run(init_database())
