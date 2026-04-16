from pydantic import Field

from .base import Base


class Location(Base):
    name: str = Field(max_length=200)
