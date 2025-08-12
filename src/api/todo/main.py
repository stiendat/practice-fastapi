from fastapi import APIRouter, HTTPException, Body
from uuid import UUID
from src.models.todo_models import TodoCreate, TodoUpdate, Todo
from src.utils.db_utils import create_todo, list_todos, update_todo, delete_todo

router = APIRouter()

@router.post("/todos", response_model=Todo, status_code=201)
def api_create_todo(todo: TodoCreate):
    return create_todo(todo)

@router.get("/todos", response_model=list[Todo])
def api_list_todos():
    return list_todos()

@router.put("/todos/{todo_id}", response_model=Todo)
def api_update_todo(todo_id: UUID, todo: TodoUpdate = Body(...)):
    if not todo.dict(exclude_unset=True):
        raise HTTPException(status_code=422, detail="At least one field must be provided for update")
    updated = update_todo(todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@router.delete("/todos/{todo_id}", status_code=200)
def api_delete_todo(todo_id: UUID):
    success = delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
