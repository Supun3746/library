from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from basic_auth.crud import get_auth
from models.book import Book
from .schemas import CreateBook, GetBook, UpdateBook


async def create_book(
    session: AsyncSession,
    book: CreateBook,
):

    book = Book(**book.model_dump())
    session.add(book)
    await session.commit()
    return book


async def get_books(session: AsyncSession, book: GetBook):
    book = book.model_dump()
    stmt = select(Book)
    if book["author_id"]:
        stmt = stmt.where(Book.author_id.ilike(f"%{book['author_id']}%"))
    if book["genre"]:
        stmt = stmt.where(Book.genre.ilike(f"%{book['genre']}%"))
    if book["title"]:
        stmt = stmt.where(Book.title.ilike(f"%{book['title']}%"))
    res = await session.execute(stmt)
    books = res.scalars().all()
    return books


async def get_books_id(session: AsyncSession, id: int):
    return await session.get(Book, id)


async def update_book(
    session: AsyncSession,
    update_book: UpdateBook,
    book: Book = Depends(get_books_id),
):
    for name, value in update_book.model_dump().items():
        setattr(book, name, value)
    await session.commit()
    return book


async def delete_book(
    session: AsyncSession,
    book: Book = Depends(get_books_id),
):
    await session.delete(book)
    await session.commit()
