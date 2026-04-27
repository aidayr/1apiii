from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.locations import Location


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        with self._database.session() as session:
            location = self._repo.get_by_id(session, location_id)
            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Такой локации не существует",
                )
            self._repo.delete(session, location_id)
            session.commit()
