from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.categoriesModel import Category


class CategoryRepository:
    def __init__(self):
        self._model: type[Category] = Category

    def get_by_id(self, session: Session, category_id: int) -> Category | None:
        query = session.query(self._model).where(self._model.id == category_id)

        return query.scalar()

    def get_all(self, session: Session) -> list[Category]:
        return session.query(Category).all()

    def create(
        self, session: Session, title: str, description: str, slug: str
    ) -> Category:
        category = self._model(
            title=title,
            description=description,
            slug=slug,
        )
        session.add(category)
        session.flush()
        return category

    def delete(self, session: Session, category_id: int) -> None:
        category = self.get_by_id(session, category_id)
        if category:
            session.delete(category)
            session.flush()
