import logging

from src.core.exceptions.database_exceptions import PostNotFound
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import PostResponse

logger = logging.getLogger(__name__)


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponse:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session, post_id)
                return PostResponse.model_validate(post)
            except PostNotFound as err:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.detail)
                raise error from err
