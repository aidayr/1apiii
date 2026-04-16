from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.postsModel import Post
from src.schemas.posts import PostRequest


class PostRepository:
    def __init__(self):
        self._model: type[Post] = Post

    def get_by_id(self, session: Session, post_id: int) -> Post | None:
        query = session.query(self._model).where(self._model.id == post_id)

        return query.scalar()

    def get_all(self, session: Session) -> list[Post]:
        return session.query(Post).all()

    def get_by_author(self, session: Session, author_id: int) -> list[Post] | None:
        query = session.query(self._model).where(self._model.id == author_id)
        return query.scalar()

    def create(self, session: Session, post_data: PostRequest) -> Post:
        post = self._model(
            title=post_data.title,
            text=post_data.text,
            author_id=post_data.author_id,
            location_id=post_data.location_id,
            category_id=post_data.category_id,
        )
        session.add(post)
        session.flush()
        return post

    def delete(self, session: Session, post_id: int) -> None:
        post = self.get_by_id(session, post_id)
        if post:
            session.delete(post)
            session.flush()
