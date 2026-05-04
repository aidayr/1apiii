from src.core.exceptions.database_exceptions import LocationNotFound
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.locations import Location


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        with self._database.session() as session:
            try:
                location = self._repo.get_by_id(session, location_id)
                return Location.model_validate(location)
            except LocationNotFound as err:
                raise LocationNotFoundByIdException(id=location_id) from err
