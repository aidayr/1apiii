from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.users import LoginUserResponse


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[LoginUserResponse]:
        async with self._database.session() as session:
            users = await self._repo.get_all(session=session)
            return [LoginUserResponse.model_validate(obj=user) for user in users]
