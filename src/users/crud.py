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
from utils import check_password
from fastapi import HTTPException, status, Depends
from typing import TYPE_CHECKING
from users.schemas import CreateUser, UserSchema
import logging


async def create_user(user_in: CreateUser, session: AsyncSession):
    try:
        async with session.begin():
            stat = select(User).filter(User.email == user_in.email)
            result = await session.execute(stat)
            existing_user = result.scalars().first()
            if existing_user:
                raise ValueError("Пользователь с такой почтой уже существует")

            user = User(**user_in.dict())
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


async def get_user_by_email(email: str, session: AsyncSession):
    try:
        stat = select(UserSchema).where(UserSchema.email == email)
        result = await session.execute(stat)
        check_user = result.scalars().first()
        if check_user:
            return check_user
        else:
            raise ValueError("Не удалось найти такого пользователя")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# async def get_current_user(token: Annotated[str, Depends])

async def check_user(session: AsyncSession, email: str, password: str):
    user = await get_user_by_email(email, session)
    if user and check_password(password, user.password):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный email или пароль")

async def get_current_user(token: str = Depends()):
    from routes import oauth2_scheme
    token = oauth2_scheme(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token=token)
        user = payload.get("sub")
        if user is None:
            raise credentials_exception
        token_data = TokenData(user=user)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.user)
    if user is None:
        raise credentials_exception
    return user
