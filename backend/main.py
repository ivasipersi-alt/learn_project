from fastapi import FastAPI, HTTPException
from backend import crud
from backend.database import init_db
from backend.schemas import CourseCreate, CourseUpdate, CoursePatch, CourseResponse

app = FastAPI(title="Online School API", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/courses", response_model=list[CourseResponse], tags=["Courses"])
def read_courses(): return crud.get_all_courses()

@app.get("/courses/{id}", response_model=CourseResponse, tags=["Courses"])
def read_course(id: int):
    c = crud.get_course_by_id(id)
    if not c: raise HTTPException(status_code=404, detail="Курс не найден")
    return c

@app.post("/courses", response_model=CourseResponse, status_code=201, tags=["Courses"])
def add_course(course: CourseCreate): return crud.create_course(course.model_dump())

@app.put("/courses/{id}", response_model=CourseResponse, tags=["Courses"])
def edit_course(id: int, course: CourseUpdate):
    res = crud.update_course(id, course.model_dump())
    if not res: raise HTTPException(status_code=404, detail="Курс не найден")
    return res

@app.patch("/courses/{id}", response_model=CourseResponse, tags=["Courses"])
def patch_course(id: int, course: CoursePatch):
    res = crud.patch_course(id, course.model_dump(exclude_none=True))
    if not res: raise HTTPException(status_code=404, detail="Курс не найден")
    return res

@app.delete("/courses/{id}", tags=["Courses"])
def delete_course(id: int):
    if not crud.delete_course(id): raise HTTPException(status_code=404, detail="Курс не найден")
    return {"message": "Успешно удалено"}