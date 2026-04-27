from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostResponse


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self) -> list[PostResponse]:
        with self._database.session() as session:
            posts = self._repo.get_all(session)
            result = []
            for post in posts:
                author = self._user_repo.get_by_id(session, post.author_id)
                result.append(
                    PostResponse(
                        id=post.id,
                        title=post.title,
                        text=post.text,
                        author_name=author.username or author.email
                        if author
                        else "Unknown",
                        location_name=None,
                        category_name=None,
                    )
                )
        return result
