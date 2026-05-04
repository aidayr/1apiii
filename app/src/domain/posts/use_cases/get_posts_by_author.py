from src.core.exceptions.database_exceptions import UserNotFoundById
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
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
        try:
            with self._database.session() as session:
                author = self._user_repo.get_by_id(session, author_id)
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
        except UserNotFoundById as err:
            raise UserNotFoundByIdException(id=author_id) from err
