import os
import sys
import jwt
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
from datetime import timedelta, datetime
from config import settings
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from typing import TYPE_CHECKING, Optional
from config import SECRET_KEY, settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
def check_password(plained_password: str, hashed_password: str):
    return pwd_context.verify(plained_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=settings.auth_jwt.algorithm)
    return encoded_jwt