from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, timezone, datetime
from models import User

router = APIRouter(
    prefix='/auth', 
    tags=["Authentication"],
)

SECRET_KEY = "jgt5e3595er9nrscvrk75pgcxolh23ca"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=('bcrypt'), deprecated = 'auto')
outh2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



def auth_user(username: str, password:str, db: db_dependency):
    user = db.query(User).where(User.username == username).first()
    if user == None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

class CreateUserRequest(BaseModel):
    username: str
    email: str
    name: str
    last_name: str
    password: str  

class Token(BaseModel):
    access_token: str
    token_type: str
 
async def get_current_user(token: Annotated[str, Depends(outh2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or Id is invalid.")
        return {"userneme": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid.")

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    user = User(
        username = request.username,
        email = request.email,
        name = request.name,
        last_name = request.last_name,
        hashed_password = bcrypt_context.hash(request.password)
    )
    db.add(user)
    db.commit()

@router.post(path='/token', response_model= Token)
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = auth_user(form.username, form.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found.')
    token = create_access_token(user.username, user.id, timedelta(minutes=60))
    return {"access_token":token,
            "token_type": "bearer"}