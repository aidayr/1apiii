from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import PostNotFoundById
from src.infrastructure.sqlite.models.postsModel import Post
from src.schemas.posts import PostRequest


class PostRepository:
    def __init__(self):
        self._model: type[Post] = Post

    def get_by_id(self, session: Session, post_id: int) -> Post:
        query = select(self._model).where(self._model.id == post_id)
        post = session.scalar(query)
        if not post:
            raise PostNotFoundById(id=post_id)
        return post

    def get_all(self, session: Session) -> list[Post]:
        return list(session.scalars(select(self._model)).all())

    def get_by_author(self, session: Session, author_id: int) -> list[Post]:
        query = select(self._model).where(self._model.author_id == author_id)
        return list(session.scalars(query).all())

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

    def update(self, session: Session, post_id: int, post_data: PostRequest) -> Post:
        post = self.get_by_id(session, post_id)
        post.title = post_data.title
        post.text = post_data.text
        post.location_id = post_data.location_id
        post.category_id = post_data.category_id
        session.flush()
        session.refresh(post)
        return post

    def delete(self, session: Session, post_id: int) -> None:
        post = self.get_by_id(session, post_id)
        session.delete(post)
        session.flush()
