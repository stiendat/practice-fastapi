from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.books import router as books_router
from src.api.users import router as users_router
from src.api.rentals import router as rentals_router

router = APIRouter()

# Include existing routers
router.include_router(hello_world_router)

# Include library management routers
router.include_router(books_router, prefix="/api/v1")
router.include_router(users_router, prefix="/api/v1")
router.include_router(rentals_router, prefix="/api/v1")
