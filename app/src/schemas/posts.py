from pydantic import Field

from .base import Base
from .categories import Category
from .locations import Location
from .users import LoginUserRequest


class PostRequest(Base):
    title: str = Field(max_length=200)
    text: str = Field(max_length=200)
    location: Location | None = None
    category: Category | None = None
    author: LoginUserRequest


class PostResponse(Base):
    post_text: str
    author_name: str
