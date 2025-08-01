import sqlite3
import os
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/simple-users", tags=["simple-users"])


class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str = None


def get_db_connection():
    """Get SQLite database connection"""
    db_path = os.path.abspath("library.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_users():
    """Get all users using direct SQLite connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, full_name, email, phone FROM users")
        users = cursor.fetchall()
        
        users_list = []
        for user in users:
            users_list.append({
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "phone": user["phone"]
            })
        
        conn.close()
        return users_list
    
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user_by_id(user_id: int):
    """Get user by ID using direct SQLite connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, full_name, email, phone FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        
        user_dict = {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user["phone"]
        }
        
        conn.close()
        return user_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/", response_model=Dict[str, Any])
async def create_user(user_data: UserCreate):
    """Create new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (full_name, email, phone) VALUES (?, ?, ?)",
            (user_data.full_name, user_data.email, user_data.phone)
        )
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # Get the created user
        cursor.execute("SELECT id, full_name, email, phone FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        user_dict = {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user["phone"]
        }
        
        conn.close()
        return user_dict
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete user by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user has active rentals
        cursor.execute("SELECT id FROM rentals WHERE user_id = ? AND is_returned = 0", (user_id,))
        active_rentals = cursor.fetchall()
        
        if active_rentals:
            conn.close()
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete user with {len(active_rentals)} active rentals"
            )
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return {"message": f"User {user_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats/summary")
async def get_users_stats():
    """Get users statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total users count
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total = cursor.fetchone()["total"]
        
        # Get users with active rentals
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) as active_users 
            FROM rentals 
            WHERE is_returned = 0
        """)
        active_users = cursor.fetchone()["active_users"]
        
        conn.close()
        
        return {
            "total_users": total,
            "active_users": active_users,
            "inactive_users": total - active_users,
            "database": "SQLite",
            "status": "✅ Working"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")