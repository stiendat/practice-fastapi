import sqlite3
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/simple-rentals", tags=["simple-rentals"])


class RentalCreate(BaseModel):
    user_id: int
    book_id: int
    days_to_return: int = 14  # Default 2 weeks


class RentalReturn(BaseModel):
    rental_id: Optional[int] = None
    book_id: Optional[int] = None


def get_db_connection():
    """Get SQLite database connection"""
    db_path = os.path.abspath("library.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_rentals():
    """Get all rentals with book and user details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.id, r.user_id, r.book_id, 
                r.rental_date, r.due_date, r.return_date, r.is_returned,
                u.full_name, u.email,
                b.title, b.author
            FROM rentals r
            JOIN users u ON r.user_id = u.id
            JOIN books b ON r.book_id = b.id
            ORDER BY r.rental_date DESC
        """)
        rentals = cursor.fetchall()
        
        rentals_list = []
        for rental in rentals:
            rentals_list.append({
                "id": rental["id"],
                "user_id": rental["user_id"],
                "book_id": rental["book_id"],
                "rental_date": rental["rental_date"],
                "due_date": rental["due_date"],
                "return_date": rental["return_date"],
                "is_returned": bool(rental["is_returned"]),
                "user": {
                    "full_name": rental["full_name"],
                    "email": rental["email"]
                },
                "book": {
                    "title": rental["title"],
                    "author": rental["author"]
                }
            })
        
        conn.close()
        return rentals_list
    
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/active", response_model=List[Dict[str, Any]])
async def get_active_rentals():
    """Get all active (not returned) rentals"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.id, r.user_id, r.book_id, 
                r.rental_date, r.due_date, r.return_date, r.is_returned,
                u.full_name, u.email,
                b.title, b.author,
                CASE 
                    WHEN date(r.due_date) < date('now') THEN 1 
                    ELSE 0 
                END as is_overdue
            FROM rentals r
            JOIN users u ON r.user_id = u.id
            JOIN books b ON r.book_id = b.id
            WHERE r.is_returned = 0
            ORDER BY r.due_date ASC
        """)
        rentals = cursor.fetchall()
        
        rentals_list = []
        for rental in rentals:
            rentals_list.append({
                "id": rental["id"],
                "user_id": rental["user_id"],
                "book_id": rental["book_id"],
                "rental_date": rental["rental_date"],
                "due_date": rental["due_date"],
                "is_overdue": bool(rental["is_overdue"]),
                "user": {
                    "full_name": rental["full_name"],
                    "email": rental["email"]
                },
                "book": {
                    "title": rental["title"],
                    "author": rental["author"]
                }
            })
        
        conn.close()
        return rentals_list
    
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/rent", response_model=Dict[str, Any])
async def rent_book(rental_data: RentalCreate):
    """Rent a book to a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id, full_name FROM users WHERE id = ?", (rental_data.user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if book exists and has available quantity
        cursor.execute("SELECT id, title, quantity FROM books WHERE id = ?", (rental_data.book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")
        
        if book["quantity"] <= 0:
            conn.close()
            raise HTTPException(status_code=400, detail="Book not available")
        
        # Check if user already has this book rented
        cursor.execute("""
            SELECT id FROM rentals 
            WHERE user_id = ? AND book_id = ? AND is_returned = 0
        """, (rental_data.user_id, rental_data.book_id))
        existing_rental = cursor.fetchone()
        
        if existing_rental:
            conn.close()
            raise HTTPException(status_code=400, detail="User already has this book rented")
        
        # Calculate due date
        rental_date = datetime.now()
        due_date = rental_date + timedelta(days=rental_data.days_to_return)
        
        # Create rental
        cursor.execute("""
            INSERT INTO rentals (user_id, book_id, rental_date, due_date, is_returned)
            VALUES (?, ?, ?, ?, 0)
        """, (rental_data.user_id, rental_data.book_id, rental_date.isoformat(), due_date.isoformat()))
        
        rental_id = cursor.lastrowid
        
        # Update book quantity
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (rental_data.book_id,))
        
        conn.commit()
        
        # Get the created rental
        cursor.execute("""
            SELECT 
                r.id, r.user_id, r.book_id, 
                r.rental_date, r.due_date, r.return_date, r.is_returned,
                u.full_name, b.title
            FROM rentals r
            JOIN users u ON r.user_id = u.id
            JOIN books b ON r.book_id = b.id
            WHERE r.id = ?
        """, (rental_id,))
        rental = cursor.fetchone()
        
        rental_dict = {
            "id": rental["id"],
            "user_id": rental["user_id"],
            "book_id": rental["book_id"],
            "rental_date": rental["rental_date"],
            "due_date": rental["due_date"],
            "is_returned": bool(rental["is_returned"]),
            "user_name": rental["full_name"],
            "book_title": rental["title"],
            "message": f"Book '{rental['title']}' rented to {rental['full_name']} until {due_date.strftime('%Y-%m-%d')}"
        }
        
        conn.close()
        return rental_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/return", response_model=Dict[str, Any])
async def return_book(return_data: RentalReturn):
    """Return a book"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        rental = None
        
        if return_data.rental_id:
            # Find by rental ID
            cursor.execute("""
                SELECT 
                    r.id, r.user_id, r.book_id, r.is_returned,
                    u.full_name, b.title
                FROM rentals r
                JOIN users u ON r.user_id = u.id
                JOIN books b ON r.book_id = b.id
                WHERE r.id = ?
            """, (return_data.rental_id,))
            rental = cursor.fetchone()
        elif return_data.book_id:
            # Find active rental by book ID
            cursor.execute("""
                SELECT 
                    r.id, r.user_id, r.book_id, r.is_returned,
                    u.full_name, b.title
                FROM rentals r
                JOIN users u ON r.user_id = u.id
                JOIN books b ON r.book_id = b.id
                WHERE r.book_id = ? AND r.is_returned = 0
                ORDER BY r.rental_date DESC
                LIMIT 1
            """, (return_data.book_id,))
            rental = cursor.fetchone()
        
        if not rental:
            conn.close()
            raise HTTPException(status_code=404, detail="Active rental not found")
        
        if rental["is_returned"]:
            conn.close()
            raise HTTPException(status_code=400, detail="Book already returned")
        
        # Update rental
        return_date = datetime.now()
        cursor.execute("""
            UPDATE rentals 
            SET return_date = ?, is_returned = 1 
            WHERE id = ?
        """, (return_date.isoformat(), rental["id"]))
        
        # Update book quantity
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = ?", (rental["book_id"],))
        
        conn.commit()
        
        return_dict = {
            "rental_id": rental["id"],
            "user_id": rental["user_id"],
            "book_id": rental["book_id"],
            "return_date": return_date.isoformat(),
            "user_name": rental["full_name"],
            "book_title": rental["title"],
            "message": f"Book '{rental['title']}' returned by {rental['full_name']}"
        }
        
        conn.close()
        return return_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats/summary")
async def get_rentals_stats():
    """Get rentals statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total rentals
        cursor.execute("SELECT COUNT(*) as total FROM rentals")
        total = cursor.fetchone()["total"]
        
        # Active rentals
        cursor.execute("SELECT COUNT(*) as active FROM rentals WHERE is_returned = 0")
        active = cursor.fetchone()["active"]
        
        # Overdue rentals
        cursor.execute("""
            SELECT COUNT(*) as overdue 
            FROM rentals 
            WHERE is_returned = 0 AND date(due_date) < date('now')
        """)
        overdue = cursor.fetchone()["overdue"]
        
        # Most popular books
        cursor.execute("""
            SELECT b.title, b.author, COUNT(*) as rental_count
            FROM rentals r
            JOIN books b ON r.book_id = b.id
            GROUP BY r.book_id
            ORDER BY rental_count DESC
            LIMIT 5
        """)
        popular_books = cursor.fetchall()
        
        popular_list = []
        for book in popular_books:
            popular_list.append({
                "title": book["title"],
                "author": book["author"],
                "rental_count": book["rental_count"]
            })
        
        conn.close()
        
        return {
            "total_rentals": total,
            "active_rentals": active,
            "returned_rentals": total - active,
            "overdue_rentals": overdue,
            "popular_books": popular_list,
            "database": "SQLite",
            "status": "✅ Working"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")