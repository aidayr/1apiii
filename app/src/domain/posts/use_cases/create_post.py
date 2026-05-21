import logging

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByNameException,
    LocationNotFoundByNameException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
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
        with self._database.session() as session:
            location_id = None
            location_name = None
            if post_data.location_name:
                location = self._location_repo.get_by_name(
                    session, post_data.location_name
                )
                if not location:
                    error = LocationNotFoundByNameException(
                        name=post_data.location_name
                    )
                    logger.error(error.detail)
                    raise error
                location_id = location.id
                location_name = location.name

            category_id = None
            category_name = None
            if post_data.category_name:
                category = self._category_repo.get_by_name(
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
            post = self._repo.create(
                session,
                title=post_data.title,
                text=post_data.text,
                author_id=current_user_id,
                location_id=location_id,
                category_id=category_id,
            )
            session.commit()
            session.refresh(post)

            return PostResponse(
                id=post.id,
                title=post.title,
                text=post.text,
                author_name=current_user_name,
                location_name=location_name,
                category_name=category_name,
            )
