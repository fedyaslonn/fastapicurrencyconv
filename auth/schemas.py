from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Optional[str] = "Bearer"

class TokenHeaders(BaseModel):
    Authorization: str

class TokenData(BaseModel):
    user: Optional[EmailStr] = None