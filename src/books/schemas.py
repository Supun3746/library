from datetime import date

from pydantic import BaseModel, ConfigDict


class BaseBook(BaseModel):
    title: str
    author_id: int
    genre: str
    available: bool
    published: date
    user_id: int


class CreateBook(BaseBook):
    pass


class GetBook(BaseModel):
    title: str | None = None
    author_id: int | None = None
    genre: str | None = None


class UpdateBook(BaseBook):
    pass


class Book(BaseBook):
    model_config = ConfigDict(from_attributes=True)
    id: int
