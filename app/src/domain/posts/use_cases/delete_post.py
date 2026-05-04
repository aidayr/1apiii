from src.core.exceptions.database_exceptions import PostNotFoundById
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        try:
            with self._database.session() as session:
                self._repo.get_by_id(session, post_id)
                self._repo.delete(session, post_id)
                session.commit()
        except PostNotFoundById as err:
            raise PostNotFoundByIdException(id=post_id) from err
