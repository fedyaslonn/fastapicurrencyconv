from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, Field, Extra

class CreateUser(BaseModel):
    username: str = Field(min_length=5, max_length=25)
    email: EmailStr
class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra=Extra.allow)

    username: str
    hashed_password: str
    email: EmailStr | None = None
    active: bool = True
