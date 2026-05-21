import logging

from src.core.exceptions.database_exceptions import UserNotFound
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import LoginUserResponse

logger = logging.getLogger(__name__)


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, user_id: int, cur_user: LoginUserResponse
    ) -> LoginUserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.get_by_id(session, user_id)
                return LoginUserResponse.model_validate(user)
            except UserNotFound as err:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(
                    f"Пользователь {cur_user.username} произвел ошибку: {error.detail}"
                )
                raise error from err
