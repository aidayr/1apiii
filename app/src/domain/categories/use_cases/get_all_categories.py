from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.categories import Category


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> list[Category]:
        with self._database.session() as session:
            categories = self._repo.get_all(session)
            return [Category.model_validate(category) for category in categories]
