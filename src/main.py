import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request

from basic_auth.crud import get_auth
from authors.routers import router as router_author
from books.routers import router as router_book
from models.config import Base, engine
from users.routers import router as router_user
from basic_auth.routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(title="Library", lifespan=lifespan)


# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     await get_auth(request=request)
#     response = await call_next(request)
#     return response


app.include_router(router=router_book, prefix="/book", tags=["Books"])
app.include_router(router=router_author, prefix="/author", tags=["Author"])
app.include_router(router=router_user, prefix="/user", tags=["User"])
app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
