from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    LocationAlreadyExists,
    LocationNotFound,
)
from src.infrastructure.sqlite.models.locationsModel import Location


class LocationRepository:
    def __init__(self):
        self._model: type[Location] = Location

    def get_by_id(self, session: Session, location_id: int) -> Location:
        query = select(self._model).where(self._model.id == location_id)
        location = session.scalar(query)
        if not location:
            raise LocationNotFound()
        return location

    def get_all(self, session: Session) -> list[Location]:
        query = select(self._model)
        return list(session.scalars(query).all())

    def create(self, session: Session, name: str) -> Location:
        try:
            location = self._model(name=name)
            session.add(location)
            session.flush()
            return location
        except IntegrityError as err:
            raise LocationAlreadyExists() from err

    def delete(self, session: Session, location_id: int) -> None:
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            session.flush()
