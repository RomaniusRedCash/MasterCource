from typing import Annotated
from datetime import timedelta, datetime

from pydantic import BaseModel
from jose import jwt, JWTError
from bcrypt import checkpw
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import ALGORITHM, SECRET_KEY
from auth.database.models import User
from auth.database.schemas import UserCreate
from auth.database.queries import UserObjects, get_userobjects_dependency

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


async def authorize_user(
    user_data: UserCreate,
    users: Annotated[UserObjects, get_userobjects_dependency]
):
    user = await users.get_user_by_name(user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists"
        )
    if await users.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    if await users.get_user_by_phone(user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists"
        )
    await users.create_user(user_data.model_dump())


async def authenticate_user(
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)],
    username: str,
    password: str,
) -> User | None:
    user = await users.get_user_by_name(username)
    if not user:
        return None
    if not checkpw(password.encode(), user.password.encode()):
        return None
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)]
) -> User:
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(
            token=token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise exception
        token_data = TokenData(username=username)
    except JWTError:
        raise exception
    user = await users.get_user_by_name(username=token_data.username)
    if not user:
        raise exception
    return user
