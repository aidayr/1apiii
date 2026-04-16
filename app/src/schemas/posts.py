# src/schemas/posts.py
from pydantic import Field

from .base import Base


class PostRequest(Base):
    title: str = Field(max_length=200)
    text: str = Field(max_length=200)
    location_id: int | None = None
    category_id: int | None = None
    author_id: int


class PostResponse(Base):
    id: int
    title: str
    text: str
    author_name: str
    location_name: str | None = None
    category_name: str | None = None
