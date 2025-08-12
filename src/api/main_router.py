from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.todolist import todo_api

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(todo_api.router)