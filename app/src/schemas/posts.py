from pydantic import Field
from typing import Optional

from .base import Base
from .categories import Category
# from .comments import Comment
from .locations import Location
from .users import LoginUserRequest


class Post(Base):
    title: str = Field(max_length=200)
    text: str = Field(max_length=200)
    location: Optional[Location] = None
    category: Optional[Category] = None
    author: LoginUserRequest
