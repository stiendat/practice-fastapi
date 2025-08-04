from src.models.library_models import *
from src.utils.db_utils import Base, get_database_url

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import csv


def init_database(csv_file):
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")
    session = Session(bind=engine)
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')  # Specify semicolon as the delimiter
        for row in reader:
            book = Book(
                title=row["Book-Title"],
                author=row["Book-Author"],
                published_year=int(row["Year-Of-Publication"]),
                quantity=1,  # Default quantity since it's not in the CSV
            )
            session.add(book)
        session.commit()
        print("Books imported successfully.")

if __name__ == "__main__":
    init_database("./test_data/books.csv")