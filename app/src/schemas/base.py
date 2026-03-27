from pydantic import BaseModel, Field
from datetime import datetime


class Base(BaseModel):
    published: bool = Field(default=True)
    created: datetime = Field()

    class Config:
        from_attributes = True
