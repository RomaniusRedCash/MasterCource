from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    __tablename__ = "Courses"

    id: Optional[int] = Field(index=True, nullable=False, primary_key=True)
    organization: str = Field()
    name: str = Field()
    price: int = Field()
    duration: str = Field()
    format: str = Field()
    rate: float = Field()
    amount: float = Field()
    is_certificate: bool = Field()
    link: str = Field
