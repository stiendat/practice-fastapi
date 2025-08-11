import csv
from datetime import datetime
from database import SessionLocal
from models import Book

def import_books_from_csv(path):
    session = SessionLocal()
    try:
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            print("📌 Các cột trong file CSV:", reader.fieldnames)

            books = []
            for row in reader:
                # Chuẩn hóa key
                row = {k.strip().lower(): v.strip() for k, v in row.items()}

                try:
                    book = Book(
                        isbn=row['isbn'],
                        book_title=row['book-title'],
                        book_author=row.get('book-author'),
                        year_of_publication=int(row['year-of-publication']) if row['year-of-publication'].isdigit() else None,
                        publisher=row.get('publisher'),
                        image_url_s=row.get('image-url-s'),
                        image_url_m=row.get('image-url-m'),
                        image_url_l=row.get('image-url-l'),
                        quantity=int(row.get('quantity', 0)),
                        date_added=datetime.utcnow(),
                        date_changed=datetime.utcnow()
                    )
                    books.append(book)
                except Exception as row_err:
                    print(f"❗ Bỏ qua dòng do lỗi: {row_err} - {row}")

            session.add_all(books)
            session.commit()
            print(f"✅ Đã import {len(books)} sách vào database.")
    except Exception as e:
        session.rollback()
        print(f"❌ Lỗi tổng: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    import_books_from_csv("Books.csv")
