from fastapi import APIRouter
from src.api import books, book_copies, inventory, users, rentals

api_router = APIRouter(prefix="/api")

api_router.include_router(books.router)
api_router.include_router(book_copies.router)
api_router.include_router(inventory.router)
api_router.include_router(users.router)
api_router.include_router(rentals.router)
