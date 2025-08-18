import asyncio
import csv
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from src.utils.db_utils import create_database_session, create_tables
from src.models import Book, User, Rental


async def clear_existing_data(session: AsyncSession):
    """
    Clear existing data from tables in correct order.
    """
    print("Clearing existing data...")
    await session.execute(delete(Rental))
    await session.execute(delete(Book))
    await session.execute(delete(User))
    await session.commit()
    print("Existing data cleared!")


async def import_books_from_csv(session: AsyncSession):
    """
    Import books from CSV file into database.
    """
    csv_file_path = "test_data/books.csv"
    
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return
    
    print(f"Importing books from {csv_file_path}...")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        
        for row in reader:
            book = Book(
                id=row['ISBN'],
                title=row['Book-Title'],
                author=row['Book-Author'],
                year_of_publication=int(row['Year-Of-Publication']) if row['Year-Of-Publication'].isdigit() else None,
                publisher=row['Publisher'],
                image_url_s=row['Image-URL-S'],
                image_url_m=row['Image-URL-M'],
                image_url_l=row['Image-URL-L'],
                quantity=1,
                created_at=datetime.utcnow()
            )
            
            session.add(book)
        
        await session.commit()
        print(f"Successfully imported books from CSV")


async def init_database():
    """
    Initialize database: create tables and import initial data.
    """
    print("Creating database tables...")
    await create_tables()
    print("Tables created successfully!")
    
    print("Importing initial data...")
    session = await create_database_session()
    try:
        await clear_existing_data(session)
        await import_books_from_csv(session)
    finally:
        await session.close()
    
    print("Database initialization completed!")


if __name__ == "__main__":
    asyncio.run(init_database()) 