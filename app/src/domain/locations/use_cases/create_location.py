import logging

from src.core.exceptions.database_exceptions import LocationAlreadyExists
from src.core.exceptions.domain_exceptions import LocationNameIsOccupiedException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import (
    LocationRepository,
)
from src.schemas.locations import Location

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: str) -> Location:
        with self._database.session() as session:
            try:
                location = self._repo.create(session, name)
                session.commit()
                logger.info(f"Локация создана: id={location.id}, name={location.name}")
                return Location.model_validate(location)
            except LocationAlreadyExists as err:
                error = LocationNameIsOccupiedException(name=name)
                logger.error(error.detail)
                raise error from err
