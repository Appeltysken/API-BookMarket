from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import List
from .models import UserModel, User, UserCreate, UserBookResponse
from .database import get_db
import secrets
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

DATABASE_URL = "sqlite:///app./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

UserModel.__table__.create(bind=engine, checkfirst=True)

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Main Page"}

@app.get("/api/users-book", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.get("/api/users-book/{user_id}", response_model=UserBookResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {
        "id": user.id,
        "attributes": {
            "username": user.username,
            "createdAt": user.createdAt,
            "updatedAt": user.updatedAt,
            "publishedAt": user.publishedAt,
            "Fname": user.Fname,
            "Lname": user.Lname,
            "sex": user.sex,
            "email": user.email,
            "phone": user.phone,
            "reg_date": user.reg_date,
        }
    }
    
    return UserBookResponse(data=user_data, meta={})

@app.post("/api/users-book", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
