import logging

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.resources.auth import verify_password
from src.schemas.users import LoginUserResponse

logger = logging.getLogger(__name__)


class AuthenticateUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str, password: str) -> LoginUserResponse:

        with self._database.session() as session:
            user = self._repo.get_by_username(session, username)

            if not user:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(str(error))
                raise error

            if not verify_password(password, user.password):
                error = WrongPasswordException()
                logger.error(str(error))
                raise error

            return LoginUserResponse.model_validate(user)
