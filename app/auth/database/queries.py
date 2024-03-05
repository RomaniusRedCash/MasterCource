from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, insert, update, delete
from bcrypt import hashpw, gensalt

from auth.database.models import User
from database.connection import get_session


class UserObjects:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_user_by_phone(self, phone: str) -> User | None:
        if phone:
            user = await self.session.execute(
                select(User).
                where(User.phone == phone)
            )
            return user.scalars().first()

    async def get_user_by_name(self, username: str) -> User | None:
        user = await self.session.execute(
            select(User).
            where(User.username == username)
        )
        return user.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.session.execute(
            select(User).
            where(User.email == email)
        )
        return user.scalars().first()

    async def create_user(self, user_data: dict[str, str]):
        password = user_data.pop("password")
        await self.session.execute(
            insert(User).
            values(
                password=hashpw(password.encode(), gensalt()),
                **user_data
            )
        )
        await self.session.commit()

    async def update_user(self, username, user_data: dict[str, str]):
        user_data = {k: v for k, v in user_data.items() if v is not None}
        if not user_data:
            return
        user = await self.get_user_by_name(username)
        await self.session.execute(
            update(User).
            where(User.username == username).
            values(**user_data)
        )
        await self.session.commit()

    async def update_password(self, password: str, username: str):
        await self.session.execute(
            update(User).
            where(User.username == username).
            values(password=hashpw(password.encode(), gensalt()))
        )
        await self.session.commit()
    
    async def delete_user(self, username: str):
        await self.session.execute(
            delete(User).
            where(User.username == username)
        )
        await self.session.commit()


def get_userobjects_dependency(session: AsyncSession = Depends(get_session)):
    return UserObjects(session)
