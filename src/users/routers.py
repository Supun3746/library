import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, middleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from basic_auth.crud import get_auth
from models.config import get_db

from . import crud
from .schemas import GetUser, UserCreate

router = APIRouter()


@router.post("/create_user")
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await crud.create_user(session=session, user=user)


@router.post("/{user_id}/books/{book_id}", response_model=GetUser)
async def add_book_to_user(
    user_id: int, book_id: int, session: AsyncSession = Depends(get_db)
):
    return await crud.add_book_to_user(
        session=session, user_id=user_id, book_id=book_id
    )


@router.get("/books_by_user", response_model=GetUser)
async def books_by_user(id: int, session: AsyncSession = Depends(get_db)):
    return await crud.books_by_user(session=session, user_id=id)


@router.post("/{user_id}/return/{book_id}")
async def return_book(
    user_id: int,
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await crud.return_book(session=session, user_id=user_id, book_id=book_id)
