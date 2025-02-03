from fastapi import FastAPI
from database import engine
from models import Base
from routers.auth import router as auth_router
from routers.todos import router as todo_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(todo_router)


Base.metadata.create_all(bind=engine)