from src.core.exceptions.database_exceptions import CategoryNotFoundById
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.categories import Category


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                return Category.model_validate(category)
        except CategoryNotFoundById as err:
            raise CategoryNotFoundByIdException(id=category_id) from err
