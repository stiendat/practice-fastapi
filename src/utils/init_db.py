from src.models.sample_models import *  # thay bằng model thật nếu có
from src.utils.db_utils import Base, get_database_url
from sqlalchemy import create_engine


def init_database():
    url = get_database_url()
    print("Connecting to:", url)
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)
    print("✅ Tables created.")


if __name__ == "__main__":
    init_database()
