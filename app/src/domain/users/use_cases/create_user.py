from src.core.exceptions.database_exceptions import UserAlreadyExists
from src.core.exceptions.domain_exceptions import (
    EmailIsOccupiedException,
    UsernameIsOccupiedException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import LoginUserResponse, RegisterUserRequest


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, ud: RegisterUserRequest) -> LoginUserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.create(session, ud)
                return LoginUserResponse.model_validate(user)
            except UserAlreadyExists as err:
                if ud.username:
                    raise UsernameIsOccupiedException(username=ud.username) from err
                if ud.email:
                    raise EmailIsOccupiedException(email=ud.email) from err
            raise
