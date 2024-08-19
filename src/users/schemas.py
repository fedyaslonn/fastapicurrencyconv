from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, Extra

class CreateUser(BaseModel):
    username: str = Field(min_length=5, max_length=25)
    email: EmailStr
    password: str
class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra=Extra.allow)

    username: str
    hashed_password: str
    email: EmailStr
    active: bool = True
