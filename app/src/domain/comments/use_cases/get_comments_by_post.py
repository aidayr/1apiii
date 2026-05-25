# src/domain/comments/use_cases/get_comments_by_post.py
from src.core.exceptions.database_exceptions import PostNotFound
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comments import CommentRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.comments import Comment


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> list[Comment]:
        async with self._database.session() as session:
            try:
                await self._post_repo.get_by_id(session, post_id)
                comments = await self._repo.get_by_post(session, post_id)
                return comments
            except PostNotFound as err:
                raise PostNotFoundByIdException(id=post_id) from err
