from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import CommentNotFound
from src.infrastructure.sqlite.models.commentsModel import Comment


class CommentRepository:
    def __init__(self):
        self._model: type[Comment] = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Comment | None:
        query = select(self._model).where(self._model.id == comment_id)
        comment = session.scalar(query)
        if not comment:
            raise CommentNotFound()
        return comment

    def get_all(self, session: Session) -> list[Comment]:
        return list(session.scalars(select(self._model)).all())

    def get_by_post(self, session: Session, post_id: int) -> list[Comment]:
        return list(
            session.scalars(
                select(self._model).where(self._model.post_id == post_id)
            ).all()
        )

    def create(
        self, session: Session, text: str, author_id: int, post_id: int
    ) -> Comment:
        comment = self._model(
            text=text,
            author_id=author_id,
            post_id=post_id,
        )
        session.add(comment)
        session.flush()
        return comment

    def delete(self, session: Session, comment_id: int) -> None:
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            session.flush()
