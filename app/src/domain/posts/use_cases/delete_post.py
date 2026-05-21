import logging

from src.core.exceptions.database_exceptions import PostNotFound
from src.core.exceptions.domain_exceptions import (
    PermissionDeniedException,
    PostNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, current_user_id: int) -> None:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session, post_id)
            except PostNotFound as err:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.detail)
                raise error from err

            if post.author_id != current_user_id:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error

            self._repo.delete(session, post_id)
            session.commit()
