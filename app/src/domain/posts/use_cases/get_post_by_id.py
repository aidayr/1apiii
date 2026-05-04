from src.core.exceptions.database_exceptions import PostNotFoundById
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostResponse


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(self, post_id: int) -> PostResponse:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                author = self._user_repo.get_by_id(session, post.author_id)
                location_name = None
                if post.location_id:
                    location = self._location_repo.get_by_id(session, post.location_id)
                    location_name = location.name
                category_name = None
                if post.category_id:
                    category = self._category_repo.get_by_id(session, post.category_id)
                    category_name = category.name
                return PostResponse(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    author_name=author.username or author.email,
                    location_name=location_name,
                    category_name=category_name,
                )
        except PostNotFoundById as err:
            raise PostNotFoundByIdException(id=post_id) from err
