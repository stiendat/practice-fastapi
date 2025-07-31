from src.models.sample_models import *
from src.models import Book
from src.utils.db_utils import Base, get_database_url

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import os


def init_database():
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

    # Import data from CSV file
    import_books_from_csv(engine)
    print("Database initialized successfully.")


def import_books_from_csv(engine):
    csv_path = os.path.join("test_data", "books.csv")

    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        return

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            next(file)

            existing_isbns = set()

            for line_num, line in enumerate(file, start=2):
                parts = line.strip().strip('"').split('";"')
                if len(parts) < 8:
                    print(f"Skipping line {line_num}: Invalid format")
                    continue

                isbn = parts[0].strip('"')
                title = parts[1]
                author = parts[2]
                year = int(parts[3]) if parts[3].isdigit() else 0
                publisher = parts[4]
                img_url_s = parts[5]
                img_url_m = parts[6]
                img_url_l = parts[7].strip('"')

                if isbn in existing_isbns:
                    print(f"Skipping line {line_num}: Duplicate ISBN {isbn}")
                    continue

                existing_isbns.add(isbn)

                # Check if book with this ISBN already exists in database
                existing_book = session.query(
                    Book).filter(Book.isbn == isbn).first()
                if existing_book:
                    print(
                        f"Skipping line {line_num}: Book with ISBN {isbn} already exists in database")
                    continue

                book = Book(
                    isbn=isbn,
                    title=title,
                    author=author,
                    year_of_publication=year,
                    publisher=publisher,
                    img_url_s=img_url_s,
                    img_url_m=img_url_m,
                    img_url_l=img_url_l,
                    total_quantity=1,
                    available_quantity=1
                )

                session.add(book)

                # Commit in batches of 1000 for better performance
                if line_num % 1000 == 0:
                    session.commit()
                    print(f"Committed {line_num} books to database")

        session.commit()
        print(f"Successfully imported {len(existing_isbns)} books from CSV")

    except Exception as e:
        print(f"Error importing books from CSV: {e}")
        session.rollback()
    finally:
        session.close()
