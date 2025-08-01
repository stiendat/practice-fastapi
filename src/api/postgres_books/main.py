import psycopg2
import psycopg2.extras
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/postgres-books", tags=["postgres-books"])


def get_postgres_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="library_db",
            user="user",
            password="123"
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_books():
    """Get all books from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("SELECT id, title, author, year, quantity FROM books ORDER BY id")
        books = cursor.fetchall()
        
        books_list = []
        for book in books:
            books_list.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "year": book["year"],
                "quantity": book["quantity"]
            })
        
        conn.close()
        return books_list
    
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{book_id}", response_model=Dict[str, Any])
async def get_book_by_id(book_id: int):
    """Get book by ID from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("SELECT id, title, author, year, quantity FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")
        
        book_dict = {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "quantity": book["quantity"]
        }
        
        conn.close()
        return book_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats/summary")
async def get_books_stats():
    """Get books statistics from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get total books count
        cursor.execute("SELECT COUNT(*) as total FROM books")
        total = cursor.fetchone()["total"]
        
        # Get total quantity
        cursor.execute("SELECT SUM(quantity) as total_qty FROM books")
        total_qty = cursor.fetchone()["total_qty"]
        
        # Get books by decade
        cursor.execute("""
            SELECT (year/10)*10 as decade, COUNT(*) as count 
            FROM books 
            GROUP BY decade 
            ORDER BY decade
        """)
        by_decade = cursor.fetchall()
        
        decades = {}
        for row in by_decade:
            decades[f"{row['decade']}s"] = row["count"]
        
        # Get most popular authors
        cursor.execute("""
            SELECT author, COUNT(*) as book_count
            FROM books 
            GROUP BY author 
            ORDER BY book_count DESC 
            LIMIT 3
        """)
        popular_authors = cursor.fetchall()
        
        authors = []
        for author in popular_authors:
            authors.append({
                "author": author["author"],
                "book_count": author["book_count"]
            })
        
        conn.close()
        
        return {
            "total_books": total,
            "total_quantity": total_qty or 0,
            "books_by_decade": decades,
            "popular_authors": authors,
            "database": "PostgreSQL",
            "status": "✅ Working"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/", response_model=Dict[str, Any])
async def create_book(book_data: dict):
    """Create new book in PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Insert new book
        cursor.execute(
            """INSERT INTO books (title, author, year, quantity) 
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (book_data["title"], book_data["author"], book_data["year"], book_data["quantity"])
        )
        
        book_id = cursor.fetchone()["id"]
        conn.commit()
        
        # Get the created book
        cursor.execute("SELECT id, title, author, year, quantity FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        
        book_dict = {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "quantity": book["quantity"]
        }
        
        conn.close()
        return book_dict
    
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/{book_id}", response_model=Dict[str, Any])
async def update_book(book_id: int, book_data: dict):
    """Update book in PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Check if book exists
        cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Update book
        cursor.execute(
            """UPDATE books 
               SET title = %s, author = %s, year = %s, quantity = %s 
               WHERE id = %s""",
            (book_data["title"], book_data["author"], book_data["year"], 
             book_data["quantity"], book_id)
        )
        conn.commit()
        
        # Get updated book
        cursor.execute("SELECT id, title, author, year, quantity FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        
        book_dict = {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "quantity": book["quantity"]
        }
        
        conn.close()
        return book_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    """Delete book from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        # Check if book exists
        cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Check if book has active rentals
        cursor.execute("SELECT id FROM rentals WHERE book_id = %s AND is_returned = false", (book_id,))
        if cursor.fetchall():
            conn.close()
            raise HTTPException(status_code=400, detail="Cannot delete book with active rentals")
        
        # Delete book
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        conn.close()
        
        return {"message": f"Book {book_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")