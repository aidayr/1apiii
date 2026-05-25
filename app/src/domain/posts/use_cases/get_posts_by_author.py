import logging

from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.posts import PostResponse

logger = logging.getLogger(__name__)


class GetPostsByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int) -> list[PostResponse]:
        async with self._database.session() as session:
            posts = await self._repo.get_by_author(session, author_id)
            return [PostResponse.model_validate(post) for post in posts]
