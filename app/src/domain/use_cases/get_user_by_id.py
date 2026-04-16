from fastapi import HTTPException, status

from ...infrastructure.sqlite.database import database
from ...infrastructure.sqlite.repositories.users import UserRepository
from ...schemas.users import LoginUserResponse


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> LoginUserResponse:
        with self._database.session() as session:
            user = self._repo.get_by_id(session, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден",
                )
            return LoginUserResponse.model_validate(obj=user)
