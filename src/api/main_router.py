from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.book_service import router as books_router
from src.api.user_service import router as user_router
from src.api.rental_service import router as rental_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(books_router)
router.include_router(user_router)
router.include_router(rental_router)
