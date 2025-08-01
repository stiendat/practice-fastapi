from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.books.main import router as books_router
from src.api.users.main import router as users_router
from src.api.rentals.main import router as rentals_router

router = APIRouter()

# Include all routers
router.include_router(hello_world_router)
router.include_router(books_router)
router.include_router(users_router)
router.include_router(rentals_router)
