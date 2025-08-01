#!/usr/bin/env python3
"""
Script to import books from CSV file into the database
Usage: 
    python import_books.py           # Import without clearing existing data
    python import_books.py --clear   # Clear existing data before import
    python import_books.py -c        # Short form of --clear
"""

import csv
import os
import sys
import random
import argparse

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from src.models import Book, Inventory, BookCopy, BookCopyStatus
    from src.utils.db_utils import Base, get_database_url
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("This script should be run in the Docker environment where all dependencies are installed.")
    print("\nTry running:")
    print("  docker-compose exec web python import_books.py --clear")
    print("  # or")
    print("  make import-books")
    sys.exit(1)

def clear_existing_data(db_session):
    """Clear all existing book-related data"""
    try:
        print("🗑️  Clearing existing data...")
        
        # Delete in correct order to avoid foreign key constraints
        db_session.execute(text("DELETE FROM rental_items"))
        db_session.execute(text("DELETE FROM book_copies"))
        db_session.execute(text("DELETE FROM inventory"))
        db_session.execute(text("DELETE FROM books"))
        
        # Reset sequences (auto-increment counters)
        db_session.execute(text("ALTER SEQUENCE books_id_seq RESTART WITH 1"))
        db_session.execute(text("ALTER SEQUENCE book_copies_id_seq RESTART WITH 1"))
        db_session.execute(text("ALTER SEQUENCE inventory_id_seq RESTART WITH 1"))
        
        db_session.commit()
        print("✅ Existing data cleared successfully")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not clear some data: {str(e)}")
        db_session.rollback()

def clean_year(year_str):
    """Clean and convert year string to integer"""
    try:
        # Remove any non-digit characters and convert to int
        year = int(''.join(filter(str.isdigit, str(year_str))))
        # Validate reasonable year range
        if 1800 <= year <= 2030:
            return year
        return None
    except (ValueError, TypeError):
        return None

def generate_random_copies(book_id, db_session):
    """Generate random number of book copies with realistic status distribution"""
    # Generate 1-5 copies per book
    num_copies = random.randint(1, 5)
    
    # Available statuses for random assignment
    statuses = [
        BookCopyStatus.AVAILABLE,
        BookCopyStatus.BORROWED, 
        BookCopyStatus.LOST,
        BookCopyStatus.DAMAGED
    ]
    
    # Create book copies with random statuses
    copy_statuses = []
    for _ in range(num_copies):
        # Bias towards AVAILABLE status (70% chance)
        if random.random() < 0.7:
            status = BookCopyStatus.AVAILABLE
        else:
            status = random.choice(statuses[1:])  # Choose from non-available statuses
        
        copy_statuses.append(status)
        
        book_copy = BookCopy(
            book_id=book_id,
            status=status
        )
        db_session.add(book_copy)
    
    # Calculate inventory counts based on actual copy statuses
    available_copies = copy_statuses.count(BookCopyStatus.AVAILABLE)
    borrowed_copies = copy_statuses.count(BookCopyStatus.BORROWED)
    lost_copies = copy_statuses.count(BookCopyStatus.LOST)
    damaged_copies = copy_statuses.count(BookCopyStatus.DAMAGED)
    
    # Create inventory record with calculated values
    inventory = Inventory(
        book_id=book_id,
        total_copies=num_copies,
        available_copies=available_copies,
        borrowed_copies=borrowed_copies,
        lost_copies=lost_copies,
        damaged_copies=damaged_copies
    )
    db_session.add(inventory)
    
    return num_copies

def import_books_from_csv(csv_file_path: str, db_session):
    """Import books from CSV file"""
    books_imported = 0
    books_skipped = 0
    total_copies_created = 0
    
    print(f"📖 Starting import from {csv_file_path}...")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Use semicolon as delimiter based on the CSV format
        reader = csv.DictReader(file, delimiter=';')
        
        for row_num, row in enumerate(reader, 1):
            try:
                # Clean and prepare data
                isbn = row['ISBN'].strip('"').strip()
                title = row['Book-Title'].strip('"').strip()
                author = row['Book-Author'].strip('"').strip()
                year_str = row['Year-Of-Publication'].strip('"').strip()
                publisher = row['Publisher'].strip('"').strip()
                image_url_s = row['Image-URL-S'].strip('"').strip()
                image_url_m = row['Image-URL-M'].strip('"').strip()
                image_url_l = row['Image-URL-L'].strip('"').strip()
                
                # Skip if essential fields are missing
                if not isbn or not title or not author:
                    print(f"⚠️  Row {row_num}: Skipping book with missing essential data: {title}")
                    books_skipped += 1
                    continue
                
                # Check if book already exists
                existing_book = db_session.query(Book).filter(Book.ISBN == isbn).first()
                if existing_book:
                    print(f"📚 Row {row_num}: Book already exists: {title} (ISBN: {isbn})")
                    books_skipped += 1
                    continue
                
                # Clean year
                publication_year = clean_year(year_str)
                
                # Create book record
                book = Book(
                    ISBN=isbn,
                    title=title,
                    author=author,
                    publication_year=publication_year,
                    publisher=publisher if publisher else None,
                    image_url_s=image_url_s if image_url_s else None,
                    image_url_m=image_url_m if image_url_m else None,
                    image_url_l=image_url_l if image_url_l else None,
                )
                
                db_session.add(book)
                db_session.flush()  # Get the book ID
                
                # Generate random copies with realistic statuses
                num_copies = generate_random_copies(book.id, db_session)
                total_copies_created += num_copies
                books_imported += 1
                
                # Progress reporting
                if books_imported % 100 == 0:
                    print(f"📈 Progress: {books_imported} books imported, {total_copies_created} copies created...")
                    db_session.commit()
                
            except Exception as e:
                print(f"❌ Row {row_num}: Error importing book '{title}': {str(e)}")
                books_skipped += 1
                db_session.rollback()
                continue
    
    # Final commit
    db_session.commit()
    
    # Final summary
    print(f"\n🎉 Import completed!")
    print(f"📚 Books imported: {books_imported}")
    print(f"📖 Total book copies created: {total_copies_created}")
    print(f"📊 Average copies per book: {total_copies_created / books_imported if books_imported > 0 else 0:.1f}")
    print(f"⚠️  Books skipped: {books_skipped}")
    
    return books_imported, books_skipped, total_copies_created

def main():
    """Main function to run the import"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Import books from CSV file')
    parser.add_argument('--clear', '-c', action='store_true', 
                        help='Clear existing data before import')
    parser.add_argument('--csv-file', default='test_data/books.csv',
                        help='Path to CSV file (default: test_data/books.csv)')
    
    args = parser.parse_args()
    
    # Get database URL and create engine
    database_url = get_database_url()
    
    print(f"🔗 Connecting to database...")
    print(f"   Host: {'Docker container (db)' if os.getenv('DOCKER_ENV') else 'localhost'}")
    print(f"   Using psycopg3 driver for PostgreSQL connection")
    
    try:
        engine = create_engine(database_url, echo=False)
        
        # Create all tables
        Base.metadata.create_all(engine)
        print("✅ Database tables ensured")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = SessionLocal()
        
        try:
            # Clear existing data if requested
            if args.clear:
                clear_existing_data(db_session)
            
            # Check if CSV file exists
            if not os.path.exists(args.csv_file):
                print(f"❌ CSV file not found: {args.csv_file}")
                print("Please ensure the CSV file exists or specify a different path with --csv-file")
                return
            
            # Import books
            books_imported, books_skipped, total_copies = import_books_from_csv(args.csv_file, db_session)
            
            if books_imported > 0:
                print(f"\n🚀 Import successful! You can now:")
                print(f"   • View API docs: http://localhost:8000/docs")
                print(f"   • Search books: http://localhost:8000/api/books/")
                print(f"   • Available books: http://localhost:8000/api/books/available")
            
        except Exception as e:
            print(f"💥 Import failed: {str(e)}")
            db_session.rollback()
            raise
        finally:
            db_session.close()
            
    except Exception as e:
        print(f"💥 Database connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure Docker containers are running: docker-compose ps")  
        print("2. Check database logs: docker-compose logs db")
        print("3. Verify .env file has correct database credentials")
        return 1

if __name__ == "__main__":
    exit(main())
