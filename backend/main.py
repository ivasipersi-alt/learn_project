from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from backend import crud
from backend.database import init_db
from backend.schemas import CourseCreate, CourseUpdate, CoursePatch, CourseResponse

app = FastAPI(title="Online School API", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/courses", response_model=list[CourseResponse])
def read_courses(filter_type: Optional[str] = Query(None)):
    return crud.get_all_courses(filter_type=filter_type)

@app.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate):
    course_id = crud.create_course(course.model_dump())
    return crud.get_course_by_id(course_id)

@app.get("/courses/{id}", response_model=CourseResponse)
def read_course(id: int):
    res = crud.get_course_by_id(id)
    if not res: raise HTTPException(status_code=404, detail="Курс не найден")
    return res

@app.put("/courses/{id}", response_model=CourseResponse)
def put_course(id: int, course: CourseUpdate):
    res = crud.update_course(id, course.model_dump())
    if not res: raise HTTPException(status_code=404, detail="Курс не найден")
    return res

@app.patch("/courses/{id}", response_model=CourseResponse)
def patch_course(id: int, course: CoursePatch):
    res = crud.patch_course(id, course.model_dump(exclude_none=True))
    if not res: raise HTTPException(status_code=404, detail="Курс не найден")
    return res

@app.delete("/courses/{id}")
def delete_course(id: int):
    if not crud.get_course_by_id(id):
        raise HTTPException(status_code=404, detail="Курс не найден")
    crud.delete_course(id)
    return {"detail": "Курс удален"}