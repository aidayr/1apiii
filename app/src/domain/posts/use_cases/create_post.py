from fastapi import HTTPException, status

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostRequest, PostResponse


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(self, post_data: PostRequest) -> PostResponse:
        with self._database.session() as session:
            author = self._user_repo.get_by_id(session, post_data.author_id)
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Автор не найден",
                )
            location_name = None
            if post_data.location_id:
                location = self._location_repo.get_by_id(session, post_data.location_id)
                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Локация не найдена",
                    )
                location_name = location.name
            category_name = None
            if post_data.category_id:
                category = self._category_repo.get_by_id(session, post_data.category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Категория не найдена",
                    )
                category_name = category.name
            post = self._repo.create(session, post_data)
            response = PostResponse(
                id=post.id,
                title=post.title,
                text=post.text,
                author_name=author.username or author.email,
                location_name=location_name,
                category_name=category_name,
            )
            session.commit()
            session.refresh(post)
        return response
