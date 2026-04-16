from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostResponse


class GetPostByAuthorUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, author_id: int) -> list[PostResponse]:
        with self._database.session() as session:
            author = self._user_repo.get_by_id(session, author_id)
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Автор не найден",
                )
            posts = self._repo.get_by_author(session, author_id)
            return [
                PostResponse(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    author_name=author.username or author.email,
                )
                for post in posts
            ]
