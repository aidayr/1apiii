# use_cases/users/delete_user.py
from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            user = self._repo.get_by_id(session=session, user_id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователя не существует",
                )
            self._repo.delete(session=session, user=user)
            session.commit()
