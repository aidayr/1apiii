from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.schemas.categories import Category


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> list[Category]:
        async with self._database.session() as session:
            categories = await self._repo.get_all(session)
            return categories
