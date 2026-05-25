import logging

from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from src.schemas.locations import Location

logger = logging.getLogger(__name__)


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> list[Location]:
        async with self._database.session() as session:
            locations = await self._repo.get_all(session)
            return [Location.model_validate(location) for location in locations]
