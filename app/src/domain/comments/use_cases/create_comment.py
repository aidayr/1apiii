# src/domain/comments/use_cases/create_comment.py
from src.core.exceptions.database_exceptions import PostNotFound, UserNotFound
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comments import CommentRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.comments import Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, text: str, author_id: int, post_id: int) -> Comment:
        async with self._database.session() as session:
            try:
                await self._user_repo.get_by_id(session, author_id)
                await self._post_repo.get_by_id(session, post_id)
                comment = await self._repo.create(session, text, author_id, post_id)
                return Comment.model_validate(comment)
            except UserNotFound as err:
                raise UserNotFoundByIdException(id=author_id) from err
            except PostNotFound as err:
                raise PostNotFoundByIdException(id=post_id) from err
