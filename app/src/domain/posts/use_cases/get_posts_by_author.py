import logging

from src.core.exceptions.database_exceptions import PostNotFound
from src.core.exceptions.domain_exceptions import PostNotFoundByAuthorException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import PostResponse

logger = logging.getLogger(__name__)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int) -> list[PostResponse]:
        with self._database.session() as session:
            try:
                posts = self._repo.get_by_author(session, author_id)
                return [PostResponse.model_validate(post) for post in posts]
            except PostNotFound as err:
                error = PostNotFoundByAuthorException(author_id=author_id)
                logger.error(error.detail)
                raise error from err
