"""
Database initialization script for synchronous PostgreSQL
"""
from sqlalchemy import create_engine
from src.models.library_models import Book, User, Base
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import sys, os
from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

# Add project root to path
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# sys.path.insert(0, project_root)

def get_db_url():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def init_database():
    try:
        engine = create_engine(get_db_url())
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
    
    # Add sample data if tables are empty
        if session.query(User).count() == 0:
            user = User(
                full_name="Test User",
                email="test@example.com",
                phone_number="123-456-7890",
                address="123 Test Street, Test City",
                is_active=True
            )
            session.add(user)

            book = Book(
                title="Sample Book",
                author="Sample Author",
                isbn="123456789",
                publication_year=2023,
                publisher="Sample Publisher",
                category="Fiction",
                total_copies=1,
                available_copies=1,
                description="A sample book for testing"
            )
            session.add(book)
            session.commit()
        print("Database initialized with sample data")
        return True
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    init_database()