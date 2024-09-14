import secrets
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi import security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.book import Book
from models.user import User
from .schemas import UserCreate
from basic_auth.crud import pwd_context


async def create_user(session: AsyncSession, user: UserCreate):
    user.password = pwd_context.hash(user.password)
    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    res = await session.execute(stmt)
    res = res.scalars().all()
    return list(res)


async def get_user_id(session: AsyncSession, id: int):
    stmt = select(User).where(User.id == id).options(selectinload(User.books))
    res = await session.execute(stmt)
    res = res.scalars().first()
    return res


async def add_book_to_user(session: AsyncSession, user_id: int, book_id: int):
    user = await get_user_id(session=session, id=user_id)
    stmt = select(Book).where(Book.id == book_id)
    res = await session.execute(stmt)
    book_item = res.scalars().first()
    if not book_item.available:
        raise HTTPException(status_code=400, detail="Книга уже занята или недоступна.")
    book_item.available = False
    user.books.append(book_item)
    await session.commit()
    return await books_by_user(session=session, user_id=user_id)


async def books_by_user(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id).options(selectinload(User.books))
    res = await session.execute(stmt)
    result = res.scalar()
    return result


async def return_book(session: AsyncSession, user_id: int, book_id: int):
    user = await get_user_id(session=session, id=user_id)
    book = next((book for book in user.books if book.id == book_id), None)
    book.available = True
    book.user_id = -1
    user.books.remove(book)
    await session.commit()
    return {"message": "return book"}
