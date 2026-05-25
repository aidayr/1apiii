import logging

from src.core.exceptions.database_exceptions import UserNotFound
from src.core.exceptions.domain_exceptions import (
    PermissionDeniedException,
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.resources.auth import verify_password
from src.schemas.users import LoginUserResponse

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, username: str, cur_user: LoginUserResponse, password: str
    ) -> None:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_username(session, username)
            except UserNotFound as exc:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(error.detail)
                raise error from exc
            if cur_user.is_admin:
                await self._repo.delete(session, user.id)
                return
            if cur_user.username != username:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error
            if not verify_password(password, user.password):
                error = WrongPasswordException()
                logger.error(error.detail)
                raise error

            await self._repo.delete(session, user.id)
