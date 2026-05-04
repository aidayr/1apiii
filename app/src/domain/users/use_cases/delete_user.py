from src.core.exceptions.database_exceptions import UserNotFound
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.get_by_id(session, user_id)
            except UserNotFound as err:
                raise UserNotFoundByIdException(id=user_id) from err

            self._repo.delete(session, user_id)
            session.commit()
