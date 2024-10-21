import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional
from decimal import Decimal

class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str = Field(..., description="Статус заказа")
    price: int = Field(None, description="Стоимость заказа")
    price: Optional[Decimal] = Field(None, description="Стоимость заказа")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    
class OrderAdd(BaseModel):
    price: int = Field(None, description="Стоимость заказа")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    
class UpdateFilter(BaseModel):
    id: int

class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Статус заказа")
    price: Optional[int] = Field(None, description="Стоимость заказа")
    user_id: Optional[int] = Field(None, description="ID пользователя, которому принадлежит заказ")
    
class DeleteFilter(BaseModel):
    id: int