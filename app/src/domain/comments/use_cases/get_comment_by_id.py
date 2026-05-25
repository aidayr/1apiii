from src.core.exceptions.database_exceptions import CommentNotFound
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comments import CommentRepository
from src.schemas.comments import Comment


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_by_id(session, comment_id)
                return Comment.model_validate(comment)
            except CommentNotFound as err:
                raise CommentNotFoundByIdException(comment_id=comment_id) from err
