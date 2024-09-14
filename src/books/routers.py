from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from basic_auth.crud import get_auth
from models.config import get_db

from . import crud
from .schemas import Book, CreateBook, GetBook, UpdateBook

router = APIRouter()


@router.post("/create_book")
async def create_book(
    book: CreateBook,
    session: AsyncSession = Depends(get_db),
    user_auth: dict = Depends(get_auth),
):
    print(user_auth)
    if user_auth != "admin":
        raise HTTPException(
            status_code=403, detail="Только администраторы могут получить доступ."
        )
    return await crud.create_book(session=session, book=book)


@router.patch("/get_books")
async def get_books(book: GetBook, session: AsyncSession = Depends(get_db)):
    return await crud.get_books(session=session, book=book)


@router.get("/{id}")
async def get_book_id(id: int, session: AsyncSession = Depends(get_db)):
    return await crud.get_books_id(session=session, id=id)


@router.patch("/{id}")
async def update_book(
    update_book: UpdateBook,
    book: Book = Depends(get_book_id),
    session: AsyncSession = Depends(get_db),
):
    return await crud.update_book(session=session, book=book, update_book=update_book)


@router.delete("/delete_book")
async def delete_book(
    book: Book = Depends(get_book_id),
    session: AsyncSession = Depends(get_db),
):
    return await crud.delete_book(session=session, book=book)
