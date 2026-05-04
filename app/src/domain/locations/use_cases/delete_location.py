from src.core.exceptions.database_exceptions import LocationNotFound
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        try:
            with self._database.session() as session:
                self._repo.get_by_id(session, location_id)
        except LocationNotFound as err:
            raise LocationNotFoundByIdException(id=location_id) from err
        self._repo.delete(session, location_id)
        session.commit()
