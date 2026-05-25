import logging

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByNameException,
    LocationNotFoundByNameException,
)
from src.core.utils.db_error import parse_integrity_error
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.locations import LocationRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.posts import PostRequest, PostResponse

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(
        self,
        post_data: PostRequest,
        current_user_id: int,
        current_user_name: str,
    ) -> PostResponse:
        async with self._database.session() as session:
            location_id = None
            location_name = None
            category_id = None
            category_name = None

            if post_data.location_name:
                location = await self._location_repo.get_by_name(
                    session, post_data.location_name
                )
                if not location:
                    error = LocationNotFoundByNameException(
                        location_name=post_data.location_name
                    )
                    logger.error(error.detail)
                    raise error
                location_id = location.id
                location_name = location.name

            if post_data.category_name:
                category = await self._category_repo.get_by_name(
                    session, post_data.category_name
                )
                if not category:
                    error = CategoryNotFoundByNameException(
                        title=post_data.category_name
                    )
                    logger.error(error.detail)
                    raise error
                category_id = category.id
                category_name = category.title

            try:
                post = await self._repo.create(
                    session,
                    title=post_data.title,
                    text=post_data.text,
                    author_id=current_user_id,
                    location_id=location_id,
                    category_id=category_id,
                )

                return PostResponse(
                    id=post.id,
                    title=post.title,
                    text=post.text,
                    author_id=current_user_id,
                    location_name=location_name,
                    category_name=category_name,
                )
            except IntegrityError as err:
                final_cause = parse_integrity_error(err)
                if final_cause == "author_id":
                    logger.error(f"User with ID {current_user_id} not found")
                else:
                    logger.error(f"Unexpected integrity error: {err}")
                raise
