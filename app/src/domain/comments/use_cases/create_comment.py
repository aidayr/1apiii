from src.core.exceptions.database_exceptions import PostNotFoundById, UserNotFound
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.comments import Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, text: str, author_id: int, post_id: int) -> Comment:
        try:
            with self._database.session() as session:
                self._user_repo.get_by_id(session, author_id)
                self._post_repo.get_by_id(session, post_id)
                comment = self._repo.create(session, text, author_id, post_id)
                session.commit()
                return Comment.model_validate(comment)
        except UserNotFound as err:
            raise UserNotFoundByIdException(id=author_id) from err
        except PostNotFoundById as err:
            raise PostNotFoundByIdException(id=post_id) from err
