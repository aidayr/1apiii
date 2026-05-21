import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFound,
    LocationNotFound,
    PostNotFound,
    UserNotFound,
)
from src.core.utils.db_error import parse_integrity_error
from src.infrastructure.sqlite.models.postsModel import Post
from src.schemas.posts import PostRequest

logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(self):
        self._model: type[Post] = Post

    def get_by_id(self, session: Session, post_id: int) -> Post:
        query = select(self._model).where(self._model.id == post_id)
        post = session.scalar(query)
        if not post:
            raise PostNotFound()
        return post

    def get_all(self, session: Session) -> list[Post]:
        return list(session.scalars(select(self._model)).all())

    def get_by_author(self, session: Session, author_id: int) -> list[Post]:
        posts = list(
            session.scalars(
                select(self._model).where(self._model.author_id == author_id)
            ).all()
        )
        if not posts:
            raise PostNotFound()
        return posts

    def create(
        self,
        session: Session,
        title: str,
        text: str,
        author_id: int,
        location_id: int | None = None,
        category_id: int | None = None,
    ) -> Post:
        try:
            post = self._model(
                title=title,
                text=text,
                author_id=author_id,
                location_id=location_id,
                category_id=category_id,
            )
            session.add(post)
            session.flush()
            return post
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "author_id":
                raise UserNotFound() from err
            elif final_cause == "location_id":
                raise LocationNotFound() from err
            elif final_cause == "category_id":
                raise CategoryNotFound() from err

    def update(self, session: Session, post_id: int, post_data: PostRequest) -> Post:
        post = self.get_by_id(session, post_id)
        post.title = post_data.title
        post.text = post_data.text
        post.location_id = post_data.location_id
        post.category_id = post_data.category_id
        try:
            session.flush()
            session.refresh(post)
            return post
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "location_id":
                raise LocationNotFound() from err
            elif final_cause == "category_id":
                raise CategoryNotFound() from err

    def delete(self, session: Session, post_id: int) -> None:
        post = self.get_by_id(session, post_id)
        session.delete(post)
        session.flush()
