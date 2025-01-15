from pydantic import BaseModel
from fastapi import FastAPI, Body, HTTPException, Path, Query
from starlette import status 
from typing import Optional
from datetime import datetime

app = FastAPI()

#external data source type json improved vers.
class course(BaseModel):
    id: int
    instructor: str
    title: str
    category: str
    publish_date: str

courses_db =[
    course(id=1, instructor="John Doe", title="Python Programming", category="Programming",rating=4, publish_date="2021-01-01"),
    course(id=2, instructor="Jane Doe", title="Java Programming", category="Programming",rating=3, publish_date="2021-01-02"),
    course(id=3, instructor="Jim Doe", title="Data Science", category="Data Science",rating=5, publish_date="2021-01-03"),
    course(id=4, instructor="John Doe", title="Machine Learning", category="Data Science",rating=4, publish_date="2021-01-04"),
    course(id=5, instructor="Jack Doe", title="Web Development", category="Web Development",rating=3, publish_date="2021-01-05"),
    course(id=6, instructor="Jenny Doe", title="Android Development", category="Mobile Development",rating=5, publish_date="2021-01-06")
]

# root path
@app.get("/courses", status_code=status.HTTP_202_ACCEPTED)
async def get_all_courses():
    return courses_db

@app.get("/courses/{course_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_course_by_id(course_id: int = Path(gt=0)):
    selected_course = [course for course in courses_db if course.id == course_id]
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