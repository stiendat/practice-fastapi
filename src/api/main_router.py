from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.todos.main import router as todos_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(todos_router)
