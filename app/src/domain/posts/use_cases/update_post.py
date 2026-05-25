import logging

from src.core.exceptions.database_exceptions import (
    PostNotFound,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByNameException,
    LocationNotFoundByNameException,
    PermissionDeniedException,
    PostNotFoundByIdException,
)
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.locations import LocationRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.users import UserRepository
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
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session, post_id)
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

            if (
                post_data.location_name
                and post_data.location_name != post.location_name
            ):
                location = await self._location_repo.get_by_name(
                    session, post_data.location_name
                )
                if not location:
                    error = LocationNotFoundByNameException(
                        name=post_data.location_name
                    )
                    logger.error(error.detail)
                    raise error
                post.location_id = location.id

            if (
                post_data.category_name
                and post_data.category_name != post.category_name
            ):
                category = await self._category_repo.get_by_name(
                    session, post_data.category_name
                )
                if not category:
                    error = CategoryNotFoundByNameException(
                        title=post_data.category_name
                    )
                    logger.error(error.detail)
                    raise error
                post.category_id = category.id

            await session.flush()
            await session.refresh(post)

            return PostResponse.model_validate(post)
