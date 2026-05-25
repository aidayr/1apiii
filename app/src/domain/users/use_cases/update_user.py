import logging

from src.core.exceptions.domain_exceptions import (
    PermissionDeniedException,
    UsernameIsOccupiedException,
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.resources.auth import get_password_hash, verify_password
from src.schemas.users import LoginUserResponse, UpdateUserRequest, UpdateUserResponse

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()
        self._token_use_case = CreateAccessTokenUseCase()

    async def execute(
        self,
        username: str,
        user_data: UpdateUserRequest,
        current_user: LoginUserResponse,
    ) -> UpdateUserResponse:
        async with self._database.session() as session:
            user = await self._repo.get_by_username(session, username)
            if not user:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(error.detail)
                raise error

            if current_user.username != username:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error

            if not verify_password(user_data.current_password, user.password):
                error = WrongPasswordException()
                logger.error(error.detail)
                raise error

            if user_data.new_username and user_data.new_username != user.username:
                existing = await self._repo.get_by_username(
                    session, user_data.new_username
                )
                if existing:
                    error = UsernameIsOccupiedException(username=user_data.new_username)
                    logger.error(error.detail)
                    raise error
                user.username = user_data.new_username

            if user_data.new_password:
                user.password = get_password_hash(user_data.new_password)

            await session.commit()
            await session.refresh(user)

            new_token = await self._token_use_case.execute(username=user.username)

            return UpdateUserResponse(
                user=LoginUserResponse.model_validate(user),
                access_token=new_token,
                token_type="bearer",
            )
