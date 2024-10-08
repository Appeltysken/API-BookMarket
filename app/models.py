from sqlalchemy import Column, Integer, String, DateTime, func
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    Fname = Column(String)
    Lname = Column(String)
    sex = Column(String)
    email = Column(String)
    phone = Column(String)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    publishedAt = Column(DateTime, default=func.now())
    reg_date = Column(String)

class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    Fname: str
    Lname: str
    sex: str
    email: str
    phone: str
    reg_date: str

class User(UserBase):
    id: int
    Fname: str
    Lname: str
    sex: str
    email: str
    phone: str
    createdAt: datetime
    updatedAt: datetime
    publishedAt: datetime
    reg_date: str

    class Config:
        orm_mode = True

class UserBookResponse(BaseModel):
    data: dict
    meta: dict

    class Config:
        orm_mode = True