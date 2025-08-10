from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model.database import get_db
from model import Book

router = APIRouter()

@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).limit(20).all()
