from typing import Annotated
from datetime import timedelta

from bcrypt import checkpw
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from auth.backend import (
    Token, 
    get_current_user, 
    create_access_token, 
    authenticate_user,
    authorize_user
)
from auth.database.schemas import UserCreate, UserUpdate, UserData
from auth.database.queries import UserObjects, get_userobjects_dependency
from auth.database.models import User
from config import ACCESS_TOKEN_EXPIRE_MINUTES, denylist

router = APIRouter()


@router.post(
    path="/register",
    responses={
        201: {"description": "Done"},
        409: {"description": "Name Conflict"}
    }
)
async def sign_up(
    form_data: Annotated[UserCreate, Depends()],
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)],
):
    await authorize_user(form_data, users)
    return JSONResponse(
        content=form_data.model_dump(exclude=["password"]), 
        status_code=status.HTTP_201_CREATED
    )


@router.post(
    path="/token",
    responses={400: {"description": "Wrong input"}}
)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)]
) -> Token:
    user = await authenticate_user(
        users=users, 
        username=form_data.username, 
        password=form_data.password
    )
    if not user:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Incorrect username or password"
    )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, 
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/profiles/{login}", response_model=UserData)
async def get_user_profile(
    login: str,
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)]
):
    user = await users.get_user_by_name(login)
    exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not user:
        raise exception
    if not user.is_public:
        raise exception
    return user


@router.get("/me", response_model=UserData)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.patch(
    path="/me", 
    response_model=UserData,
    responses={409: {"Description": "Name Conflict"}}
)
async def update_me(
    current_user: Annotated[User, Depends(get_current_user)],
    form_data: UserUpdate,
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)],
):
    user_data = form_data.model_dump()
    try:
        await users.update_user(current_user.username, user_data)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return await users.get_user_by_name(form_data.username)


@router.post("/me/updatePassword")
async def update_password(
    current_user: Annotated[User, Depends(get_current_user)],
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)],
    old_password: str,
    new_password: str
):
    if not checkpw(old_password.encode(), current_user.password.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await users.update_password(current_user.username, new_password)


@router.delete("/me/delete")
async def delete_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
    users: Annotated[UserObjects, Depends(get_userobjects_dependency)],
):
    await users.delete_user(current_user.username)
