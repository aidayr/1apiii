from pydantic import Field
from .base import Base


class Category(Base):
    title: str = Field(max_length=200)
    description: str
    slug: str
    is_published: bool = True
