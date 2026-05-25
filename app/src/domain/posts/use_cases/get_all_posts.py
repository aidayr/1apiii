import logging

from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.posts import PostResponse

logger = logging.getLogger(__name__)


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> list[PostResponse]:
        async with self._database.session() as session:
            posts = await self._repo.get_all(session)
            return [PostResponse.model_validate(post) for post in posts]
