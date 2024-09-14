import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from models.config import get_db
from models.user import User

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def basic_auth(
    session: AsyncSession,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or passsword",
        headers={"WWW-Authenticate": "Basic"},
    )
    stmt = select(User).filter(
        User.username == credentials.username,
    )
    res = await session.execute(stmt)
    user = res.scalar()
    if not user or not pwd_context.verify(credentials.password, user.password):
        return unauthed_exc
    return user.username


async def get_auth(
    credentials: HTTPBasicCredentials = Depends(security), session=Depends(get_db)
):
    # credentials = await security(request=request)
    return await basic_auth(credentials=credentials, session=session)
