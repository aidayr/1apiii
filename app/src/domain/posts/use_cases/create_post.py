from src.core.exceptions.database_exceptions import (
    CategoryNotFoundById,
    LocationNotFoundById,
    UserNotFoundById,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostRequest, PostResponse


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(self, post_data: PostRequest) -> PostResponse:
        try:
            with self._database.session() as session:
                author = self._user_repo.get_by_id(session, post_data.author_id)
                location_name = None
                if post_data.location_id:
                    location = self._location_repo.get_by_id(
                        session, post_data.location_id
                    )
                    location_name = location.name
                category_name = None
                if post_data.category_id:
                    category = self._category_repo.get_by_id(
                        session, post_data.category_id
                    )
                    category_name = category.name
                post = self._repo.create(session, post_data)
                session.commit()
                return PostResponse(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    author_name=author.username or author.email,
                    location_name=location_name,
                    category_name=category_name,
                )
        except UserNotFoundById as err:
            raise UserNotFoundByIdException(id=post_data.author_id) from err
        except LocationNotFoundById as err:
            raise LocationNotFoundByIdException(id=post_data.location_id) from err
        except CategoryNotFoundById as err:
            raise CategoryNotFoundByIdException(id=post_data.category_id) from err
