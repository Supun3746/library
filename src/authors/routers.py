from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.config import get_db

from . import crud
from .schemas import CreateAuthor

router = APIRouter()


@router.post("/crate_author")
async def create_author(author: CreateAuthor, session: AsyncSession = Depends(get_db)):
    return await crud.create_author(session=session, author=author)


@router.get("/get_authors")
async def get_authors(session: AsyncSession = Depends(get_db)):
    return await crud.get_authors(session=session)


@router.get("/get_author{id}")
async def get_author_id(id: int, session: AsyncSession = Depends(get_db)):
    return await crud.get_author_id(session=session, id=id)


@router.get("/get_books_by_author")
async def get_books_by_author(author_id: int, session: AsyncSession = Depends(get_db)):
    return await crud.get_books_by_author(session=session, author_id=author_id)
