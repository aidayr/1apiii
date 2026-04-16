from fastapi import HTTPException

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
        with self._database.session() as session:
            author = self._user_repo.get_by_id(session, author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Автор не найден")

            post = self._post_repo.get_by_id(session, post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            comment = self._repo.create(session, text, author_id, post_id)
            session.commit()
            session.refresh(comment)
            return Comment.model_validate(comment)
