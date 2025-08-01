import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.library_models import Book
from commands.init_database.main import get_sync_database_url


def import_books_from_csv():
    """Import books from CSV file into database using sync approach"""
    print("Starting CSV import...")
    
    try:
        # Create sync database connection
        database_url = get_sync_database_url()
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
                print(f"✅ Successfully imported {books_added} books from CSV")
                
    except FileNotFoundError:
        print("❌ Error: test_data/books.csv file not found")
        raise
    except Exception as e:
        print(f"❌ Error importing CSV: {e}")
        raise


def import_data():
    """Import data from CSV file"""
    import_books_from_csv()