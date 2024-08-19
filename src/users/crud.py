import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../auth/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/users/')))
print(sys.path)
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from typing import Annotated
from utils import check_password, hash_password
from fastapi import HTTPException, status, Depends
from typing import TYPE_CHECKING
from users.schemas import CreateUser, UserSchema
import logging
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import get_session
from config import SECRET_KEY
import jwt

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

async def create_user(user_in: CreateUser, session: AsyncSession):
    try:
        async with session.begin():
            stat = select(User).filter(User.email == user_in.email)
            result = await session.execute(stat)
            existing_user = result.scalars().first()
            if existing_user:
                raise ValueError("Пользователь с такой почтой уже существует")
            hashed_password = hash_password(user_in.password)
            user_data = user_in.dict()
            user_data["password"] = hashed_password
            user = User(**user_data)
            session.add(user)

        await session.refresh(user)

    except IntegrityError as e:
        raise ValueError("Не удалось создать пользователя")

    except Exception as e:
        raise e

    return {
        "success": True,
        "user": user
    }


async def get_user(username: str, session: AsyncSession):
    try:
        stat = select(User).where(User.username == username)
        result = await session.execute(stat)
        check_user = result.scalars().first()
        if check_user:
            return check_user
        else:
            raise ValueError("Не удалось найти такого пользователя")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# async def get_current_user(token: Annotated[str, Depends])

async def check_user(session: AsyncSession, username: str, password: str):
    user = await get_user(username, session)
    if user and check_password(password, user.password):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный username или пароль")

async def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.auth_jwt.algorithm])
        username = payload.get("username")
        print(f"Decoded token: {payload}")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user(username=username, session=session)
    if user is None:
        raise credentials_exception
    return user
