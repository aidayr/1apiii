import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryAlreadyExists,
    CategoryNotFound,
)
from src.infrastructure.sqlite.models.categoriesModel import Category

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self):
        self._model: type[Category] = Category

    def get_by_id(self, session: Session, category_id: int) -> Category:
        category = session.scalar(
            select(self._model).where(self._model.id == category_id)
        )
        if not category:
            raise CategoryNotFound()
        return category

    def get_by_name(self, session: Session, name: str) -> Category | None:
        return session.scalar(select(self._model).where(self._model.title == name))

    def get_all(self, session: Session) -> list[Category]:
        return list(session.scalars(select(self._model)).all())

    def create(
        self, session: Session, title: str, description: str, slug: str
    ) -> Category:
        try:
            category = self._model(title=title, description=description, slug=slug)
            session.add(category)
            session.flush()
            return category
        except IntegrityError as err:
            raise CategoryAlreadyExists() from err

    def delete(self, session: Session, category_id: int) -> None:
        category = self.get_by_id(session, category_id)
        session.delete(category)
        session.flush()
