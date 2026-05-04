from pydantic import Field

from .base import Base


class Category(Base):
    id: int
    title: str = Field(max_length=200)
    description: str
    slug: str
