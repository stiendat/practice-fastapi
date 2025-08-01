from src.models.library_models import Book, User, Rental
from src.utils.db_utils import Base
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB

from sqlalchemy import create_engine


def get_sync_database_url() -> str:
    return f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"


def init_database():
    database_url = get_sync_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")
    print("Tables created: books, users, rentals")
