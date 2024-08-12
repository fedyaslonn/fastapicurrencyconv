import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../auth/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../users/')))
from utils import encode_jwt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas import TokenInfo
from users import crud
from users.schemas import CreateUser, UserSchema
from passlib.context import CryptContext
from .crud import check_user, get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from typing import Annotated

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="get_token")

@users_router.post("/create_user")
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    return await crud.create_user(user_in=user, session=session)

@users_router.post("/login", response_model=TokenInfo)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    user = await check_user(session, form_data.email, form_data.password)
    access_token = encode_jwt(data={"sub":user.email})
    return TokenInfo(access_token=access_token, token_type="Bearer")


