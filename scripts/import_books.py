
import asyncio
import sys
import csv
import os

# Fix for Windows: "Psycopg cannot use the 'ProactorEventLoop' to run in async mode"
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add the root directory of the project to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Book  # Import through the models package
from src.utils.db_utils import session_factory
from sqlalchemy.exc import IntegrityError

async def import_books_from_csv():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'books.csv')

    if not os.path.exists(file_path):
        print(f"Error: The file doesn't exist at {file_path}")
        return

    books_to_add = []
    async with session_factory() as session:
        with open(file_path, mode='r', encoding='latin-1') as csvfile: # Use 'latin-1' encoding to handle special characters
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            header = next(reader)

            for row in reader:
                try:
                    row_data = dict(zip(header, row))

                    # Check if the book already exists in the database
                    existing_book = await session.get(Book, row_data['ISBN'])
                    if existing_book:
                        continue
                    
                    year_of_pub = int(row_data['Year-Of-Publication']) if row_data['Year-Of-Publication'].isdigit() else None

                    book = Book(
                        isdn=row_data['ISBN'],
                        book_title=row_data['Book-Title'],
                        book_author=row_data['Book-Author'],
                        year_of_pub=year_of_pub,
                        publisher=row_data['Publisher'],
                        image_url_s=row_data['Image-URL-S'],
                        image_url_m=row_data['Image-URL-M'],
                        image_url_l=row_data['Image-URL-L']
                    )
                    books_to_add.append(book)

                except (ValueError, KeyError) as e:
                    print(f"Bỏ qua dòng bị lỗi: {row}. Lỗi: {e}")
                    continue
        
        if books_to_add:
            print(f"Đang thêm {len(books_to_add)} sách mới vào database...")
            session.add_all(books_to_add)
            try:
                await session.commit()
                print(f"Thành công! Đã import {len(books_to_add)} sách.")
            except IntegrityError as e:
                await session.rollback()
                print(f"Lỗi IntegrityError: {e}. Giao dịch đã được rollback.")
            except Exception as e:
                await session.rollback()
                print(f"Lỗi không xác định: {e}. Giao dịch đã được rollback.")
        else:
            print("Không có sách mới nào để thêm. Database đã được cập nhật.")


if __name__ == "__main__":
    # Chạy hàm async bằng asyncio.run()
    asyncio.run(import_books_from_csv())
