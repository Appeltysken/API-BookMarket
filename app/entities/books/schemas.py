from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional
from decimal import Decimal

class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=75, description="Название книги")
    author_id: Optional[int] = Field(None, description="ID автора произведения")
    genre: Optional[str] = Field(None, max_length=70, description="Жанр произведения")
    publisher: Optional[str] = Field(None, max_length=70, description="Издательство")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги")
    price: Optional[Decimal] = Field(None, description="Цена книги")
    book_picture: Optional[str] = Field(None, description="Название изображения автора")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    
    @validator('price')
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class BookAdd(BaseModel):
    name: str = Field(..., min_length=1, max_length=75, description="Название книги")
    price: int = Field(None, description="Стоимость заказа")
    author_id: Optional[int] = Field(None, description="ID автора произведения")
    genre: Optional[str] = Field(None, max_length=70, description="Жанр произведения")
    publisher: Optional[str] = Field(None, max_length=70, description="Издательство")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги")
    price: Optional[Decimal] = Field(None, description="Цена книги")
    
    @validator('price')
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class UpdateFilter(BaseModel):
    id: int

class BookUpdate(BaseModel):
    price: Optional[int] = Field(None, description="Стоимость заказа")
    author_id: Optional[int] = Field(None, description="ID автора произведения")
    genre: Optional[str] = Field(None, max_length=70, description="Жанр произведения")
    publisher: Optional[str] = Field(None, max_length=70, description="Издательство")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги")
    price: Optional[Decimal] = Field(None, description="Цена книги")
    
    @validator('price')
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class DeleteFilter(BaseModel):
    id: int

class BookPhoto(BaseModel):
    id: int
    book_picture: str = Field(None, description="Название изображения книги")