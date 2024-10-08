from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

# URL для базы данных
DATABASE_URL = "sqlite:///app./test.db"

# Создание базы данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()

# Создание сессии базы данных
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()