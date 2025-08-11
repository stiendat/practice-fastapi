from src.models.todo_models import TodoModel
from src.dto.todo_dto import TodoCreateDTO, TodoUpdateDTO, TodoDTO
from src.repository.base_repository import BaseRepository

class TodoRepository(BaseRepository[TodoModel, TodoCreateDTO, TodoUpdateDTO]):
    """
    Repository for managing TodoModel entities.
    Inherits from BaseRepository to provide CRUD operations.
    """

    def __init__(self):
        super().__init__(TodoModel)


todo_repository = TodoRepository()