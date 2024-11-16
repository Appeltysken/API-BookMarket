import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional
from decimal import Decimal

class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str = Field(..., description="Статус заказа")
    price: Optional[Decimal] = Field(None, description="Стоимость заказа")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    books_id: int = Field(..., description="ID книги, которая заказана")
    
    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class OrderAdd(BaseModel):
    price: int = Field(None, description="Стоимость заказа")
    books_id: int = Field(..., description="ID книги, которая заказана")
    
    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class UpdateFilter(BaseModel):
    id: int

class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Статус заказа")
    price: Optional[int] = Field(None, description="Стоимость заказа")
    
    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value
    
class DeleteFilter(BaseModel):
    id: int