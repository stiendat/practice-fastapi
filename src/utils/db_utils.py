from typing import Dict, List
from uuid import UUID, uuid4
from datetime import datetime
from src.models.todo_models import Todo, TodoCreate, TodoUpdate

todos_db: Dict[str, Todo] = {}

def create_todo(todo_create: TodoCreate) -> Todo:
    todo_id = uuid4()
    now = datetime.now()
    todo = Todo(
        id=todo_id,
        title=todo_create.title,
        completed=todo_create.completed,
        created_at=now,
        updated_at=now,
    )
    todos_db[str(todo_id)] = todo
    return todo

def list_todos() -> List[Todo]:
    return list(todos_db.values())

def update_todo(todo_id: UUID, todo_update: TodoUpdate) -> Todo | None:
    todo_key = str(todo_id)
    if todo_key not in todos_db:
        return None
    stored = todos_db[todo_key]
    update_data = todo_update.dict(exclude_unset=True)
    updated_todo = stored.copy(update=update_data)
    updated_todo.updated_at = datetime.now()
    todos_db[todo_key] = updated_todo
    return updated_todo

def delete_todo(todo_id: UUID) -> bool:
    todo_key = str(todo_id)
    if todo_key in todos_db:
        del todos_db[todo_key]
        return True
    return False
