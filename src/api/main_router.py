from fastapi import APIRouter
from src.api.todo.main import router as todo_router

router = APIRouter()

router.include_router(todo_router)
