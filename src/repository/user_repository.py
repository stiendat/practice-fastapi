from src.models.user_models import UserModel
from src.dto.user_dto import UserCreateDTO, UserUpdateDTO
from src.repository.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[UserModel, UserCreateDTO, UserUpdateDTO]):
    def __init__(self):
        super().__init__(UserModel)
        logger.debug("UserRepository initialized")


user_repository = UserRepository()