from pathlib import Path
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional
import secrets

BASE_DIR = Path(__file__).parent.parent
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

class DBSettings(BaseSettings):
    host: str = DB_HOST
    port: str = DB_PORT
    name: str = DB_NAME
    user: str = DB_USER
    password: str = DB_PASS

class AuthJWT(BaseModel):
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()

settings = Settings()

secret_key = secrets.token_urlsafe(32)

SECRET_KEY = secret_key