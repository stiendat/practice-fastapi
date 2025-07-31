from fastapi import APIRouter
from src.api import books, rentals, users
router = APIRouter()
router.include_router(books.router, prefix="/books", tags=["Books"])
router.include_router(rentals.router, prefix="/rentals", tags=["Rentals"])
router.include_router(users.router, prefix="/users", tags=["Users"])
