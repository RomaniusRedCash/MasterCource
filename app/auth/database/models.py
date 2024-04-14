from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "Users"

    id: Optional[int] = Field(nullable=False, primary_key=True, index=True)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(max_length=50, unique=True, index=True)
    password: str = Field()
    phone: str = Field(max_length=20, unique=True)
    image: str = Field(max_length=200)
    registered_at: datetime = Field(default=datetime.now())
    favourate_subjects: str = Field()
    spesialized: str = Field()
    hobbies: str = Field()
    is_superuser: bool = Field(default=False)
    is_active: bool = Field(default=True)
