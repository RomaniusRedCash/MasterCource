from fastapi import APIRouter, Depends

from courses.database.queries import CoursesObjects, get_CoursesObjects_dependensy
from courses.database.models import Course

router = APIRouter(prefix="/courses")


@router.get("/courses-list", response_model=Course)
async def get_courses_list():
    pass