from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.users.main import router as users_router
from src.api.books.main import router as books_router
from src.api.rentals.main import router as rentals_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(books_router, prefix="/books", tags=["books"])
router.include_router(rentals_router, prefix="/rentals", tags=["rentals"])