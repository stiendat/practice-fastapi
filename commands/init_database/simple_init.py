# PostgreSQL connection for Docker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys, os
import pandas as pd

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

def get_db_url():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def connect_postgres():
    try:
        engine = create_engine(get_db_url())
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connected to PostgreSQL")
        return True
    except:
        print("Cannot connect to PostgreSQL")
        return False

def create_tables():
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        from src.models.library_models import Base
        engine = create_engine(get_db_url())
        Base.metadata.create_all(engine)
        print("Tables created")
        return True
    except:
        print("Cannot create tables")
        return False

def check_book_database_empty():
    try:
        from src.models.library_models import Book
        
        engine = create_engine(get_db_url())
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        book_count = session.query(Book).count()
        session.close()
        
        print(f"Books in database: {book_count}")
        return book_count == 0
        
    except Exception as e:
        print(f"Error checking database: {e}")
        return False

def insert_books_from_csv():
    try:
        from src.models.library_models import Book
        
        engine = create_engine(get_db_url())
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "test_data", "books.csv")
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            session.close()
            return False
        
        df = pd.read_csv(csv_path, delimiter=';')
        print(f"Found {len(df)} books in CSV, importing all...")

        books_added = 0
        for index, row in df.iterrows():
            try:
                book = Book(
                    title=str(row.get('Book-Title', '')).strip(),
                    author=str(row.get('Book-Author', '')).strip(),
                    isbn=str(row.get('ISBN', f'ISBN-{index}')).strip(),
                    publication_year=int(row.get('Year-Of-Publication', 2000)) if pd.notna(row.get('Year-Of-Publication')) else None,
                    publisher=str(row.get('Publisher', '')).strip() if pd.notna(row.get('Publisher')) else None,
                    image_url_s=str(row.get('Image-URL-S', '')).strip() if pd.notna(row.get('Image-URL-S')) else None,
                    image_url_m=str(row.get('Image-URL-M', '')).strip() if pd.notna(row.get('Image-URL-M')) else None,
                    image_url_l=str(row.get('Image-URL-L', '')).strip() if pd.notna(row.get('Image-URL-L')) else None,
                    is_available=True
                )
                session.add(book)
                books_added += 1
                session.commit()
            
            except Exception as e:
                print(f"Error adding book at row {index}: {e}")
                continue
        
        session.commit()
        session.close()
        print(f"Successfully imported {books_added} books from CSV")
        return True
        
    except Exception as e:
        print(f"Error importing books from CSV: {e}")
        return False

def main():
    print("=== Init Database ===")
    print(f"Database URL: postgresql://{POSTGRES_USER}:***@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    
    if connect_postgres():
        if create_tables():
            if check_book_database_empty():
                print("Database is empty, importing CSV data...")
                if insert_books_from_csv():
                    print("CSV import completed successfully!")
                else:
                    print("CSV import failed!")
            else:
                print("Database already has data, skipping CSV import")
        else:
            print("Failed to create tables!")
    else:
        print("Failed to connect to PostgreSQL!")
    print("Done!")

if __name__ == "__main__":
    main()
