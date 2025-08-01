import sqlite3
import os
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/simple-books", tags=["simple-books"])


def get_db_connection():
    """Get SQLite database connection"""
    db_path = os.path.abspath("library.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_books():
    """Get all books using direct SQLite connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, author, year, quantity FROM books")
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
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{book_id}", response_model=Dict[str, Any])
async def get_book_by_id(book_id: int):
    """Get book by ID using direct SQLite connection"""
    from fastapi import HTTPException
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, author, year, quantity FROM books WHERE id = ?", (book_id,))
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
    """Get books statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        
        conn.close()
        
        return {
            "total_books": total,
            "total_quantity": total_qty,
            "books_by_decade": decades,
            "database": "SQLite",
            "status": "✅ Working"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")