from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.database import Base

if TYPE_CHECKING:
    from .commentsModel import Comment
    from .postsModel import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")
    comments: Mapped[list[Comment]] = relationship("Comment", back_populates="author")
