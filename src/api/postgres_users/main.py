import psycopg2
import psycopg2.extras
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/postgres-users", tags=["postgres-users"])


class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str = None


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
async def get_all_users():
    """Get all users from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("SELECT id, full_name, email, phone FROM users ORDER BY id")
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


@router.post("/", response_model=Dict[str, Any])
async def create_user(user_data: UserCreate):
    """Create new user in PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert new user
        cursor.execute(
            """INSERT INTO users (full_name, email, phone) 
               VALUES (%s, %s, %s) RETURNING id""",
            (user_data.full_name, user_data.email, user_data.phone)
        )
        
        user_id = cursor.fetchone()["id"]
        conn.commit()
        
        # Get the created user
        cursor.execute("SELECT id, full_name, email, phone FROM users WHERE id = %s", (user_id,))
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
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats/summary")
async def get_users_stats():
    """Get users statistics from PostgreSQL"""
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get total users count
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total = cursor.fetchone()["total"]
        
        # Get users with active rentals
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) as active_users 
            FROM rentals 
            WHERE is_returned = false
        """)
        active_users = cursor.fetchone()["active_users"]
        
        conn.close()
        
        return {
            "total_users": total,
            "active_users": active_users or 0,
            "inactive_users": total - (active_users or 0),
            "database": "PostgreSQL",
            "status": "✅ Working"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")