from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.simple_books.main import router as simple_books_router
from src.api.simple_users.main import router as simple_users_router
from src.api.simple_rentals.main import router as simple_rentals_router
from src.api.postgres_books.main import router as postgres_books_router
from src.api.postgres_users.main import router as postgres_users_router
from src.api.postgres_rentals.main import router as postgres_rentals_router

router = APIRouter()

router.include_router(hello_world_router)
# SQLite versions
router.include_router(simple_books_router)
router.include_router(simple_users_router)
router.include_router(simple_rentals_router)
# PostgreSQL versions
router.include_router(postgres_books_router)
router.include_router(postgres_users_router)
router.include_router(postgres_rentals_router)
