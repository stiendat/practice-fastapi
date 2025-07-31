from src.models.sample_models import *
from src.models.user_models import *
from src.models.borrowing_models import *
from src.models.book_models import *
from src.utils.db_utils import Base, get_database_url

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import uuid

def init_database():
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

def import_books_from_csv(csv_file_path):
    """
    Import books data from CSV file into the database
    """
    # Create database connection
    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Read CSV with semicolon delimiter
            csv_reader = csv.DictReader(file, delimiter=';')

            books_imported = 0

            for row in csv_reader:
                # Check if book with this ISBN already exists
                existing_book = session.query(BookModel).filter_by(ISBN=row['ISBN']).first()
                if existing_book:
                    print(f"Book with ISBN {row['ISBN']} already exists, skipping...")
                    continue

                # Create new book instance
                book = BookModel(
                    id=uuid.uuid4(),
                    ISBN=row['ISBN'],
                    book_title=row['Book-Title'],
                    book_author=row['Book-Author'],
                    year_of_publication=int(row['Year-Of-Publication']) if row[
                        'Year-Of-Publication'].isdigit() else None,
                    publisher=row['Publisher'],
                    image_url_s=row['Image-URL-S'],
                    image_url_L=row['Image-URL-L'],
                    # Set default quantities for library management
                    total_quantity=1,
                    available_quantity=1
                )

                session.add(book)
                books_imported += 1

            # Commit all changes
            session.commit()
            print(f"Successfully imported {books_imported} books into the database.")

    except Exception as e:
        print(f"Error importing books: {str(e)}")
        session.rollback()
    finally:
        session.close()