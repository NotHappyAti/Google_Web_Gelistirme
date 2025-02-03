from fastapi import Depends, APIRouter, status, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, ToDo
from typing import Annotated, Optional
from routers.auth import get_current_user

router = APIRouter(
    prefix="/todo", 
    tags=["ToDo"]
)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/")
def get_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(ToDo).where(ToDo.user_id == user.get("id")).all()

@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
def get_by_id(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    item = db.query(ToDo).filter(ToDo.id == id).where(ToDo.user_id == user.get("id")).first()
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_item(user: user_dependency, todo: ToDoRequest, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    item = ToDo(**todo.model_dump(), user_id = user.get('id'))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_item(user: user_dependency, todo_req: ToDoRequest, db: db_dependency, id: int = Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == id).where(ToDo.user_id == user.get("id")).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_item_by_id(user: user_dependency, db:db_dependency, id: int =Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == id).where(ToDo.user_id == user.get("id")).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(todo)
    db.commit()