from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .config import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="user")
