from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.books import router as books_router
from src.api.borrowers import router as borrowers_router
from src.api.borrowing import router as borrowing_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(books_router)
router.include_router(borrowers_router)
router.include_router(borrowing_router)
