from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Path, Query
from starlette import status
from typing import Optional, List

app = FastAPI()

class Course(BaseModel):
    idnum: int
    instructor: str
    title: str
    rating: int
    publish_year: int

class courseRequest(BaseModel):
    idnum: Optional[int] = None
    instructor: str = Field(min_length=3, max_length=50)
    title: str = Field(min_length=3, max_length=50)
    rating: int = Field(gte=0, lte=5)
    publish_year: int = Field(gte=2000, lte=2100)

    model_config = {
        "json_schema_extra": {
            'example': {
                "instructor": "Example Instructor",
                "title": "Example Title",
                "rating": 4,
                "publish_year": 2022
            }
        }
    }

courses_db = [
    Course(idnum=1, instructor="John Doe", title="Python Programming", rating=4, publish_year=2023),
    Course(idnum=2, instructor="Jane Doe", title="Java Programming", rating=3, publish_year=2021),
    Course(idnum=3, instructor="Jim Doe", title="Data Science", rating=5, publish_year=2024),
    Course(idnum=4, instructor="John Doe", title="Machine Learning", rating=4, publish_year=2020),
    Course(idnum=5, instructor="Jack Doe", title="Web Development", rating=3, publish_year=2021),
    Course(idnum=6, instructor="Jenny Doe", title="Android Development", rating=5, publish_year=2021),
]

# root path
@app.get("/courses", status_code=status.HTTP_202_ACCEPTED)
async def get_all_courses():
    return courses_db

@app.get("/courses/{course_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_course_by_id(course_id: int = Path(gt=0)):
    selected_course = [course for course in courses_db if course.idnum == course_id]
    if selected_course:
        return selected_course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')


@app.get("/courses/", status_code=status.HTTP_202_ACCEPTED)
async def get_course_by_rating(rating: int = Query(gt=0, lt=6)):
    selected_course = [course for course in courses_db if course.rating == rating]
    if selected_course:
        return selected_course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')

@app.put("/courses/create_course", status_code=status.HTTP_201_CREATED)
async def create_course(course_request: courseRequest):
    course = course_request.model_dump()
    course = Course(**find_id(course))
    courses_db.append(course)
    return None
    
def find_id(course):
    course['idnum'] = 1 if len(courses_db) == 0 else courses_db[-1].idnum + 1
    return course

@app.put("/courses/update_course", status_code=status.HTTP_204_NO_CONTENT)
async def update_course(course: courseRequest):
    changed = False
    for i in range(len(courses_db)):
        if courses_db[i].idnum == course.idnum:
            courses_db[i] = course
            changed = True
            break
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details= "Course not found.")
    
@app.delete("/courses/delete", status_code=status.HTTP_200_OK)
async def delete_course(idnum: int):
    deleted = False
    for i in range(len(courses_db)):
        if courses_db[i].idnum == idnum:
            del courses_db[i]
            deleted = True
            break
        
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found or already removed.")