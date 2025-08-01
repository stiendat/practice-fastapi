import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.library_models import Book


def get_sqlite_database_url() -> str:
    return "sqlite:///./library.db"


def import_books_from_csv_sqlite():
    """Import books from CSV file into SQLite database"""
    print("Starting CSV import to SQLite...")

    try:
        # Create SQLite database connection
        database_url = get_sqlite_database_url()
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        with open('test_data/books.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            with SessionLocal() as session:
                books_added = 0
                for row in csv_reader:
                    # Skip the id column from CSV, let database auto-generate
                    book = Book(
                        title=row['title'],
                        author=row['author'],
                        year=int(row['year']),
                        quantity=int(row['quantity'])
                    )
                    session.add(book)
                    books_added += 1

                session.commit()
                print(f"✅ Successfully imported {books_added} books from CSV to SQLite")

    except FileNotFoundError:
        print("❌ Error: test_data/books.csv file not found")
        raise
    except Exception as e:
        print(f"❌ Error importing CSV: {e}")
        raise
