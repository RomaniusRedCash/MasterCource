from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, insert, update, delete

from courses.database.models import Course
from database.connection import get_session


class CoursesObjects:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get(self, offset, limit, *args, **kwargs) -> Course | None: 
        result = await self.session.execute(
            select(Course).
            filter(*args).
            filter_by(**kwargs).
            offset(offset).
            limit(limit)
        )
        return result.scalars().all()

    async def create(self, **data) -> Course | None:
        await self.session.execute(
            insert(Course).
            values(**data)
        )
        await self.session.commit()

    async def delete(self, *args, **data) -> None: 
        await self.session.execute(
            delete(Course).
            filter(*args)
        )
        await self.session.commit()

    async def update(self, *args, **data) -> None: 
        await self.session.execute(
            update(Course).
            filter(*args).
            values(**data)
        )
        await self.session.commit()


def get_CoursesObjects_dependensy(session: AsyncSession = Depends(get_session)):
    return CoursesObjects(session)
