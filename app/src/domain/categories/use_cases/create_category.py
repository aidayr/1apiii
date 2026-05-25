import logging

from src.core.exceptions.database_exceptions import CategoryAlreadyExists
from src.core.exceptions.domain_exceptions import CategorySlugIsOccupiedException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.schemas.categories import Category

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str, slug: str, description: str = None) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.create(session, title, description, slug)
                return Category.model_validate(category)
            except CategoryAlreadyExists as err:
                error = CategorySlugIsOccupiedException(slug=slug)
                logger.error(error.detail)
                raise error from err
