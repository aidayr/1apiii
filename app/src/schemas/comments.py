from datetime import date, datetime

from pydantic import Field

from src.schemas.base import Base
from src.schemas.posts import Post
from src.schemas.users import LoginUserRequest


class Comment(Base):
    text: str = Field(max_length=100)
    author: LoginUserRequest
    created: date = Field(default_factory=datetime.now)
    post: Post
