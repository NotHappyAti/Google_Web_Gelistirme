from fastapi import Depends, FastAPI, status, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, ToDo
from typing import Annotated, Optional

app = FastAPI()

class ToDoRequest(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    priority: int
    is_completed: Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            'example': {
                "title": "Example Title",
                "description": "Example Description",
                "priority": 1,
                "is_completed": False,
            }
        }
    }

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/read_all")
def get_all(db: db_dependency):
    return db.query(ToDo).all()

@app.get("/read/{id}", status_code=status.HTTP_200_OK)
def get_by_id(db: db_dependency, id: int = Path(gt=0)):
    item = db.query(ToDo).filter(ToDo.id == id).first()
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_item(todo: ToDoRequest, db: db_dependency):
    item = ToDo(**todo.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)  # Refresh the instance to reflect changes
    return item

@app.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_item(todo_req: ToDoRequest, db: db_dependency, id: int = Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    else:
        todo.title = todo_req.title
        todo.description = todo_req.description
        todo.priority = todo_req.priority
        todo.is_completed = todo_req.is_completed  # Handle is_completed update
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_item_by_id(db:db_dependency, id: int =Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(todo)
    db.commit()