from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.categories import Category


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str, description: str, slug: str) -> Category:
        with self._database.session() as session:
            category = self._repo.create(session, title, description, slug)
            session.commit()
            session.refresh(category)
        return Category.model_validate(category)
