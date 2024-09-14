from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book

from models.author import Author
from .schemas import CreateAuthor


async def create_author(session: AsyncSession, author: CreateAuthor):
    author = Author(**author.model_dump())
    session.add(author)
    await session.commit()
    return author


async def get_authors(session: AsyncSession):
    stmt = select(Author).order_by(Author.id)
    res = await session.execute(stmt)
    res = res.scalars().all()
    return list(res)


async def get_author_id(session: AsyncSession, id: int):
    stmt = select(Author).where(Author.id == id)
    res = await session.execute(stmt)
    res = res.scalar()
    return res


async def get_books_by_author(session: AsyncSession, author_id: int):
    stmt = select(Book).where(Book.author_id == author_id)
    res = await session.execute(stmt)
    res = res.scalars().all()
    return list(res)
