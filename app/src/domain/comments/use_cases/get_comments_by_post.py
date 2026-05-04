from src.core.exceptions.database_exceptions import PostNotFoundById
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.comments import Comment


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> list[Comment]:
        try:
            with self._database.session() as session:
                self._post_repo.get_by_id(session, post_id)
                comments = self._post_repo.get_by_post(session, post_id)
        except PostNotFoundById as err:
            raise PostNotFoundByIdException(post_id=post_id) from err
        return [Comment.model_validate(comment) for comment in comments]
