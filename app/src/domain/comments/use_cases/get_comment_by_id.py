from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.schemas.comments import Comment


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> Comment:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session, post_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Такого комментария не существует",
                )
            return Comment.model_validate(comment)
