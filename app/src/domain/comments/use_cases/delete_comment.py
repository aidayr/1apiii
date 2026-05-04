from src.core.exceptions.database_exceptions import CommentNotFoundById
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
        except CommentNotFoundById as err:
            raise CommentNotFoundByIdException(comment_id=comment_id) from err
        self._repo.delete(session, comment_id)
        session.commit()
