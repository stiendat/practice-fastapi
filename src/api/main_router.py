from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.todo import api_todo

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(api_todo.router)
