from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.locationsModel import Location


class LocationRepository:
    def __init__(self):
        self._model: type[Location] = Location

    def get_by_id(self, session: Session, location_id: int) -> Location | None:
        query = session.query(self._model).where(self._model.id == location_id)

        return query.scalar()

    def get_all(self, session: Session) -> list[Location]:
        return session.query(Location).all()

    def create(self, session: Session, name: str) -> Location:
        location = self._model(name=name)
        session.add(location)
        session.flush()
        return location

    def delete(self, session: Session, location_id: int) -> None:
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            session.flush()
