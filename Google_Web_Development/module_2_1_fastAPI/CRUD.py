from fastapi import FastAPI, Body

app = FastAPI()

#external data source type json
courses_db =[
    {
        "id": 1,
        "instructor": "John Doe",
        "title": "Python Programming",
        "category": "Programming",
    },
    {
        'id': 2,
        'instructor': 'Jane Doe',
        'title': 'Java Programming',
        'category': 'Programming',
    },
    {
        'id': 3,
        'instructor': 'Jim Doe',
        'title': 'Data Science',
        'category': 'Data Science',
    },
    {
        'id': 4,
        'instructor': 'John Doe',
        'title': 'Machine Learning',
        'category': 'Data Science',
    },
    {
        'id': 5,
        'instructor': 'Jack Doe',
        'title': 'Web Development',
        'category': 'Web Development',
    },
    {
        'id': 6,
        'instructor': 'Jenny Doe',
        'title': 'Android Development',
        'category': 'Mobile Development',
    }
]

# root path
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# get all courses
@app.get("/courses")
async def get_all_courses():
    return courses_db

# get course by id path filter
@app.get("/courses/{course_id}")
async def get_course_by_id(course_id: int):
    for course in courses_db:
        if course["id"] == course_id:
            return course
        
    return {"Error": "Course not found"}


# get course by title path filter
@app.get("/courses/{course_title}")
async def get_courses_by_title_not_working(course_title: str):
    return [course for course in courses_db if course['title'] == course_title]
# This will not work because of the uppper code block used same path parameter
# We can use query parameter instead of path parameter or we can use different path, i.e.

# get courses by title path filter
@app.get("/courses/title/{course_title}")
async def get_courses_by_title(course_title: str):
    return [course for course in courses_db if course['title'].casefold() == course_title.casefold()]

# get courses by instructor query filter
@app.get("/courses/instructor/")
async def get_courses_by_instructor(instructor: str):
    return [course for course in courses_db if course['instructor'].casefold() == instructor.casefold()] 


# get courses by instructor and title query & path filter
@app.get("/courses/{instructor}/")
async def get_courses_by_instructor_and_title(instructor: str, title: str):
    return [course for course in courses_db if course['instructor'].casefold() == instructor.casefold() and course['title'].casefold() == title.casefold()]

# Create a new course 
@app.put("/create_course")
async def create_new_course(course: dict = Body(...)):
    courses_db.append(course)
    return
# Delete a course
@app.delete("/delete_course/{course_id}")
async def delete_course(course_id: int):
    for index, course in enumerate(courses_db):
        if course['id'] == course_id:
            courses_db.pop(index)
            break

# uvicorn CRUD:app --reload