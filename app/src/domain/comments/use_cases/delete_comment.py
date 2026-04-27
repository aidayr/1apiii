from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session, comment_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Комментарий не найден",
                )
            self._repo.delete(session, comment_id)
            session.commit()
