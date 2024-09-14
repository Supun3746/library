from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///sqlite3.db"
    echo: bool = False


settings = Settings()

engine = create_async_engine(settings.url)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with session_factory() as session:
        yield session
