from typing import Optional
from pydantic import BaseModel, Field

class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Название курса")
    description: str = Field(default="", max_length=500, description="Описание программы")
    price: float = Field(..., ge=0, description="Стоимость курса")
    duration_months: int = Field(..., gt=0, description="Длительность в месяцах")
    instructor: str = Field(..., min_length=2, max_length=100, description="Преподаватель")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CoursePatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, ge=0)
    duration_months: Optional[int] = Field(default=None, gt=0)
    instructor: Optional[str] = Field(default=None, min_length=2, max_length=100)

class CourseResponse(CourseBase):
    id: int
