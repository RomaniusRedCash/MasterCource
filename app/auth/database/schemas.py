from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr
from fastapi import Form, Depends


class BaseUserModel(BaseModel):
    username: Annotated[str, Form(max_length=50)]
    email: Annotated[EmailStr, Form(max_length=50)]
    phone: Optional[Annotated[str | None, Form(max_length=20, pattern="\+[\d]+")]] = None
    image: Optional[Annotated[str | None, Form(max_length=200)]] = None
    is_public: Annotated[bool, Form()]


class UserData(BaseUserModel):
    registered_at: datetime
    is_active: bool
    is_superuser: bool


class UserCreate(BaseUserModel):
    password: Annotated[str, Form(max_length=100, min_length=6)]
    
    class Config:
        orm_mode = True


class UserUpdate(BaseUserModel):
    username: Optional[Annotated[str, Form(max_length=50)]] = None
    email: Optional[Annotated[EmailStr, Form(max_length=50)]] = None
    is_public: Optional[Annotated[bool, Depends()]] = None
