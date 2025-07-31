from sqlalchemy import create_engine
from src.utils.db_utils import get_database_url, Base 
from src.models import user, book, rental

def init_database():
    db_url = get_database_url(sync=True)
    print("Using DB URL:", db_url)
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    init_database()
