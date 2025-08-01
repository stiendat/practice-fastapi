import asyncio
import csv
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db_utils import engine, Base
from src.models.library_models import Book


async def import_books_from_csv():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    with open('test_data/books.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        async with AsyncSession(engine) as session:
            for row in csv_reader:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    year=int(row['year']),
                    quantity=int(row['quantity'])
                )
                session.add(book)
            
            await session.commit()
            print(f"Successfully imported books from CSV")


if __name__ == "__main__":
    asyncio.run(import_books_from_csv())