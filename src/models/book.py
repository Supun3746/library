from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config import Base

if TYPE_CHECKING:
    from .user import User


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    genre: Mapped[str]
    available: Mapped[bool]
    published: Mapped[date]
    user: Mapped["User"] = relationship(back_populates="books")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
