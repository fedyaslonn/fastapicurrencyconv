import os
import sys
import jwt
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))

from datetime import timedelta
from config import settings
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from typing import TYPE_CHECKING

def encode_jwt(payload, private_key=settings.auth_jwt.private_key_path.read_text(),
               algorithm=settings.auth_jwt.algorithm, expire_minutes=settings.auth_jwt.access_token_expire_minutes):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_minutes:
        expire = now + expire_minutes
    else:
        expire = now + timedelta(minutes=30)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded
def decode_jwt(token, public_key=settings.auth_jwt.public_key_path.read_text(),
               algorithm=settings.auth_jwt.algorithm):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        if decoded["exp"] >= time.time():
            return decoded
        else:
            return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)
def check_password(plained_password, hashed_password):
    return pwd_context.verify(plained_password, hashed_password)

def get_current_token_payload(token: Depends()):
    from users.routes import oauth2_scheme
    token = oauth2_scheme(token)
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return payload
