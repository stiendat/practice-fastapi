from fastapi import APIRouter
from src.api.books.main import router as books_router
from src.api.users.main import router as users_router
from src.api.rental.main import router as rental_router

router = APIRouter()

router.include_router(books_router, prefix="/books", tags=["books"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(rental_router, prefix="/rental", tags=["rental"])