from pydantic import BaseModel, EmailStr

from books.schemas import Book


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(BaseUser):
    pass


class GetUser(BaseModel):
    username: str
    books: list["Book"]
