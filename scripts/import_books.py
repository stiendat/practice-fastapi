"""
Script to import books data from CSV file into the database
"""

import csv
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from src.models.library_models import get_session, create_tables, Book
from src.schemas.library_schemas import BookCreate
from src.services.library_service import BookService


def import_books_from_csv(csv_file_path: str):
    """
    Import books from CSV file into the database
    """
    # Create tables if they don't exist
    create_tables()
    
    # Get database session
    db: Session = get_session()
    
    try:
        imported_count = 0
        skipped_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                try:
                    # Check if book with this ISBN already exists
                    existing_book = BookService.get_book_by_isbn(db, row['isbn'])
                    if existing_book:
                        print(f"Book with ISBN {row['isbn']} already exists. Skipping...")
                        skipped_count += 1
                        continue
                    
                    # Create book from CSV data
                    book_data = BookCreate(
                        title=row['title'].strip('"'),
                        author=row['author'].strip('"'),
                        publication_year=int(row['publication_year']),
                        isbn=row['isbn'].strip('"'),
                        quantity=int(row['quantity'])
                    )
                    
                    # Create book in database
                    book = BookService.create_book(db, book_data)
                    print(f"Imported book: {book.title} by {book.author}")
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error importing book from row {row}: {str(e)}")
                    continue
        
        print(f"\nImport completed!")
        print(f"Books imported: {imported_count}")
        print(f"Books skipped: {skipped_count}")
        
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error during import: {str(e)}")
    finally:
        db.close()


def main():
    """Main function to run the import script"""
    csv_file_path = os.path.join(project_root, "test_data", "books.csv")
    
    print("Starting book import from CSV...")
    print(f"CSV file path: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print(f"CSV file does not exist: {csv_file_path}")
        return
    
    import_books_from_csv(csv_file_path)


if __name__ == "__main__":
    main()
