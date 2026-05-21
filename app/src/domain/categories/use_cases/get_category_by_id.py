import logging

from src.core.exceptions.database_exceptions import CategoryNotFound
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import (
    CategoryRepository,
)
from src.schemas.categories import Category

logger = logging.getLogger(__name__)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_id(session, category_id)
                return Category.model_validate(category)
            except CategoryNotFound as err:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.detail)
                raise error from err
