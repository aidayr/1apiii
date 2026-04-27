from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import LoginUserResponse


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[LoginUserResponse]:
        with self._database.session() as session:
            users = self._repo.get_all(session=session)
            if not users:
                return []
            return [LoginUserResponse.model_validate(obj=user) for user in users]
