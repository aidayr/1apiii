from datetime import date, datetime

from pydantic import Field

from .base import Base
from .posts import Post
from .users import LoginUserRequest


class Comment(Base):
    text: str = Field(max_length=100)
    author: LoginUserRequest
    created: date = Field(default_factory=datetime.now)
    post: Post
