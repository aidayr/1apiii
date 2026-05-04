from src.core.exceptions.database_exceptions import CommentNotFoundById
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.schemas.comments import Comment


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> Comment:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, post_id)
        except CommentNotFoundById as err:
            raise CommentNotFoundByIdException(post_id=post_id) from err
        return Comment.model_validate(comment)
