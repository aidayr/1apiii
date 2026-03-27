from .base import Base
from .users import LoginUserRequest
from .posts import Post
from pydantic import Field
from datetime import date, datetime


class Comment(Base):
    text: str = Field(max_length=100)
    author: LoginUserRequest
    created: date = Field(default_factory=datetime.now)
    post: Post
