from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.to_do_service import router as todo_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(todo_router)
