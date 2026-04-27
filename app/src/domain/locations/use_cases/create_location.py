from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.locations import Location


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: str) -> Location:
        with self._database.session() as session:
            location = self._repo.create(session, name)
            session.commit()
            session.refresh(location)
        return Location.model_validate(location)
