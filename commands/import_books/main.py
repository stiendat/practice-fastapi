import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from src.models import Book
from src.utils.db_utils import get_database_url


def import_books():
    """Import books from CSV file into the database"""
    csv_file_path = "test_data/books.csv"
    
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return
    
    # Create database connection
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        imported_count = 0
        skipped_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # CSV uses semicolon as delimiter
            csv_reader = csv.DictReader(file, delimiter=';')
            
            for row in csv_reader:
                try:
                    # Parse year as integer, handle empty values
                    year = None
                    if row['Year-Of-Publication'].strip():
                        try:
                            year = int(row['Year-Of-Publication'])
                        except ValueError:
                            year = None
                    
                    # Create book object
                    book = Book(
                        isbn=row['ISBN'].strip(),
                        title=row['Book-Title'].strip(),
                        author=row['Book-Author'].strip(),
                        year_of_publication=year,
                        publisher=row['Publisher'].strip() if row['Publisher'].strip() else None,
                        quantity=1,  # Default quantity
                        image_url_s=row['Image-URL-S'].strip() if row['Image-URL-S'].strip() else None,
                        image_url_m=row['Image-URL-M'].strip() if row['Image-URL-M'].strip() else None,
                        image_url_l=row['Image-URL-L'].strip() if row['Image-URL-L'].strip() else None,
                    )
                    
                    session.add(book)
                    session.commit()
                    imported_count += 1
                    print(f"Imported: {book.title} by {book.author}")
                    
                except IntegrityError:
                    session.rollback()
                    skipped_count += 1
                    print(f"Skipped duplicate ISBN: {row['ISBN']}")
                except Exception as e:
                    session.rollback()
                    print(f"Error importing book {row.get('Book-Title', 'Unknown')}: {str(e)}")
                    skipped_count += 1
        
        print(f"\nImport completed!")
        print(f"Successfully imported: {imported_count} books")
        print(f"Skipped: {skipped_count} books")
        
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    import_books()
