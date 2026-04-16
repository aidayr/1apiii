from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.schemas.comments import Comment


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[Comment]:
        with self._database.session() as session:
            comments = self._repo.get_all(session)
            return [Comment.model_validate(post) for post in comments]
