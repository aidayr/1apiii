import logging

from src.core.exceptions.database_exceptions import LocationNotFound
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from src.schemas.locations import Location

logger = logging.getLogger(__name__)


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_by_id(session, location_id)
                return Location.model_validate(location)
            except LocationNotFound as err:
                error = LocationNotFoundByIdException(location_id=location_id)
                logger.error(error.detail)
                raise error from err
