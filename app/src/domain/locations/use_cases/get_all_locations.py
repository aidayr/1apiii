from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.locations import Location


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> list[Location]:
        with self._database.session() as session:
            locations = self._repo.get_all(session)
            return [Location.model_validate(location) for location in locations]
