from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comments import CommentRepository
from src.schemas.comments import Comment


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[Comment]:
        async with self._database.session() as session:
            comments = await self._repo.get_all(session)
            return [Comment.model_validate(post) for post in comments]
