from src.core.exceptions.database_exceptions import CategoryNotFoundById
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                self._repo.delete(session, category_id)
                session.commit()
        except CategoryNotFoundById as err:
            raise CategoryNotFoundByIdException(id=category_id) from err
