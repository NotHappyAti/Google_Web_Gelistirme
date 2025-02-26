from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)

class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))