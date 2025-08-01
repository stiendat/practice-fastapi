from src.models.library_models import Book, User, Rental
from src.utils.db_utils import Base
from sqlalchemy import create_engine


def get_sqlite_database_url() -> str:
    return "sqlite:///./library.db"


def init_sqlite_database():
    """Initialize SQLite database for testing"""
    database_url = get_sqlite_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("SQLite database initialized successfully.")
    print("Tables created: books, users, rentals")
    print("Database file: library.db")