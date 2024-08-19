import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../auth/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../users/')))
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import TokenInfo
from users import crud as users_crud
from users.schemas import CreateUser
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from typing import Annotated
import utils
from datetime import timedelta
from config import settings
import jwt
from config import SECRET_KEY, settings


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

token_router = APIRouter(
    tags=["Token"]
)

@users_router.post("/create_user")
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    return await users_crud.create_user(user_in=user, session=session)

@users_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    user = await users_crud.check_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    access_token_expires = timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
    access_token = utils.create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user_id": user.id,
        "username": user.username
    }
