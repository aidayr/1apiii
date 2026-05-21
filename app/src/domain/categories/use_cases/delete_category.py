import logging

from src.core.exceptions.database_exceptions import CategoryNotFound
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import (
    CategoryRepository,
)

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.get_by_id(session, category_id)
            except CategoryNotFound as err:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.detail)
                raise error from err

            self._repo.delete(session, category_id)
            session.commit()
