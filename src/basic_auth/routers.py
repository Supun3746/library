from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from . import crud


router = APIRouter()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(crud.security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }
