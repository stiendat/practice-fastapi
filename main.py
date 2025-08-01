from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.api.main_router import router as main_router
from src.utils.db_utils import get_database
from src.models.library_models import User, Book, Rental
from datetime import datetime

app = FastAPI(
    title="Library Management API with PostgreSQL",
    description="Library management system with PostgreSQL database",
    version="1.0.0"
)

# Auto-initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and import CSV data if empty"""
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from commands.init_database.simple_init import (
        connect_postgres, create_tables, 
        check_book_database_empty, insert_books_from_csv
    )
    
    if connect_postgres():
        create_tables()
        if check_book_database_empty():
            insert_books_from_csv()
        else:
            print("Database already has books, skipping")

app.include_router(main_router)

@app.get("/", operation_id="get_root")
async def root():
    return {
        "message": "Library Management API with PostgreSQL",
        "docs": "/docs",
        "database": "PostgreSQL",
        "endpoints": {
            "hello": "/hello",
            "users": "/users",
            "books": "/books",
            "rentals": "/rentals",
            "health": "/health"
        }
    }


# Health check
@app.get("/health", tags=["System"])
async def health_check(db: Session = Depends(get_database)):
    """Health check endpoint"""
    try:
        # Test database connection
        user_count = db.query(User).count()
        book_count = db.query(Book).count()
        rental_count = db.query(Rental).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow(),
            "data_count": {
                "users": user_count,
                "books": book_count,
                "rentals": rental_count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }
