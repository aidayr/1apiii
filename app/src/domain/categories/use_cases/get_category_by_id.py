import logging

from src.core.exceptions.database_exceptions import CategoryNotFound
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from src.schemas.categories import Category

logger = logging.getLogger(__name__)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_id(session, category_id)
                return Category.model_validate(category)
            except CategoryNotFound as err:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.detail)
                raise error from err
