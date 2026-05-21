import logging

from src.core.exceptions.database_exceptions import UserAlreadyExists
from src.core.exceptions.domain_exceptions import (
    UsernameIsOccupiedException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.resources.auth import get_password_hash
from src.schemas.users import LoginUserResponse, RegisterUserRequest

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user: RegisterUserRequest) -> LoginUserResponse:
        with self._database.session() as session:
            user.password = get_password_hash(password=user.password)
            try:
                user1 = self._repo.create(session, user)
            except UserAlreadyExists as err:
                error = UsernameIsOccupiedException(username=user.username)
                logger.error(error.detail)
                raise error from err
            return LoginUserResponse.model_validate(obj=user1)
