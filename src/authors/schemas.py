from datetime import date
from pydantic import BaseModel


class BaseAuthor(BaseModel):
    name: str
    birth: date


class CreateAuthor(BaseAuthor):
    pass
