import logging

from src.core.exceptions.database_exceptions import LocationNotFound
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.get_by_id(session, location_id)
            except LocationNotFound as err:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.detail)
                raise error from err

            await self._repo.delete(session, location_id)
            logger.info(f"Локация {location_id} удалена")
