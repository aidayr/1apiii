import logging

from src.core.exceptions.database_exceptions import (
    PostNotFound,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PermissionDeniedException,
    PostNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostRequest, PostResponse

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(
        self,
        post_id: int,
        post_data: PostRequest,
        current_user_id: int,
    ) -> PostResponse:
        with self._database.session() as session:
            try:
                post = self._repo.get_by_id(session, post_id)
            except PostNotFound as err:
                error = PostNotFoundByIdException(post_id=post_id)
                logger.error(error.detail)
                raise error from err

            if post.author_id != current_user_id:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error

            post.title = post_data.title
            post.text = post_data.text

            if post_data.location_name:
                location = self._location_repo.get_by_name(
                    session, post_data.location_name
                )
                if not location:
                    error = LocationNotFoundByIdException(id=0)
                    logger.error(error.detail)
                    raise error
                post.location_id = location.id
            if post_data.category_name:
                category = self._category_repo.get_by_name(
                    session, post_data.category_name
                )
                if not category:
                    error = CategoryNotFoundByIdException(id=0)
                    logger.error(error.detail)
                    raise error
                post.category_id = category.id

            session.commit()
            session.refresh(post)

            return PostResponse.model_validate(post)
