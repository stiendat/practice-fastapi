# Database initialization with sample data
from sqlalchemy import create_engine
from uuid import uuid4
from datetime import datetime
import sys, os
from src.models.library_models import User, Book, Base
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

def get_db_url():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def init_database():
    try:
        engine = create_engine(get_db_url())
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()

        # if session.query(User).count() == 0:
        #     user = User(
        #         id=uuid4(),
        #         name="Test User",
        #         email="test@example.com",
        #         created_at=datetime.now(),
        #         updated_at=datetime.now()
        #     )
        #     session.add(user)
            
        #     book = Book(
        #         id=uuid4(),
        #         title="Sample Book",
        #         author="Sample Author",
        #         isbn="123456789",
        #         is_available=True,
        #         created_at=datetime.now(),
        #         updated_at=datetime.now()
        #     )
        #     session.add(book)
        #     session.commit()
            
        # session.close()
        # print("Database initialized with sample data")
        # return True
    except:
        print("Failed to initialize database")
        return False

if __name__ == "__main__":
    init_database()
