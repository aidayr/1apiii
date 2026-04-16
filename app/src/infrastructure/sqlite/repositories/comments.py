from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.commentsModel import Comment


class CommentRepository:
    def __init__(self):
        self._model: type[Comment] = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Comment | None:
        query = session.query(self._model).where(self._model.id == comment_id)

        return query.scalar()

    def get_all(self, session: Session) -> list[Comment]:
        return session.query(Comment).all()

    def get_by_post(self, session: Session, post_id: int) -> list[Comment]:
        return session.query(Comment).where(Comment.post_id == post_id).all()

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
