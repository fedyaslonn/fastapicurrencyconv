from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = "Bearer"

class TokenHeaders(BaseModel):
    Authorization: str

class TokenData(BaseModel):
    user: Optional[EmailStr] = None