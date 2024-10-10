import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str = Field(..., description="Username должен быть номером телефона или адресом эл. почты")
    password: str = Field(..., min_lenght=8, description="Пароль пользователя")
    Fname: str = Field(None, min_lenght=1, max_length=50, description="Имя пользователя")
    Lname: str = Field(None, min_lenght=1, max_length=50,description="Фамилия пользователя")
    sex: str = Field(..., description="Пол пользователя")
    email: EmailStr = Field(None, description="Электронная почта пользователя")
    phone: str = Field(None, description="Номер телефона пользователя")
    sell_history: Optional[str] = Field(None, description="История продаж")
    buy_history: Optional[str] = Field(None, description="История покупок")
    
class UserAdd(BaseModel):
    username: str = Field(..., description="Username должен быть номером телефона или адресом эл. почты")
    password: str = Field(..., min_lenght=8, description="Пароль пользователя")
    Fname: str = Field(None, min_lenght=1, max_length=50, description="Имя пользователя")
    Lname: str = Field(None, min_lenght=1, max_length=50,description="Фамилия пользователя")
    sex: str = Field(..., description="Пол пользователя")
    email: EmailStr = Field(None, description="Электронная почта пользователя")
    phone: str = Field(None, description="Номер телефона пользователя")
    sell_history: Optional[str] = Field(None, description="История продаж")
    buy_history: Optional[str] = Field(None, description="История покупок")
    
class UpdateFilter(BaseModel):
    id: int

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Username должен быть номером телефона или адресом эл. почты")
    password: Optional[str] = Field(None, min_lenght=8, description="Пароль пользователя")
    Fname: Optional[str] = Field(None, min_lenght=1, max_length=50, description="Имя пользователя")
    Lname: Optional[str] = Field(None, min_lenght=1, max_length=50,description="Фамилия пользователя")
    sex: Optional[str] = Field(None, description="Пол пользователя")
    email: Optional[EmailStr] = Field(None, description="Электронная почта пользователя")
    phone: Optional[str] = Field(None, description="Номер телефона пользователя")
    sell_history: Optional[str] = Field(None, description="История продаж")
    buy_history: Optional[str] = Field(None, description="История покупок")

class DeleteFilter(BaseModel):
    id: int

# @validator('username')
# def validate_username(cls, value):
#     if not (re.match(r'^\S+@\S+\.\S+$', value) or re.match(r'^\d{11}$', value)):
#         raise ValueError("Username должен быть номером телефона или адресом эл. почты")
#     return value

# @validator('password')
# def validate_password(cls, value):
#     if not re.search(r'[A-Za-z]', value):
#         raise ValueError('Пароль должен содержать хотя бы одну букву')
#     if not re.search(r'\d', value):
#         raise ValueError('Пароль должен содержать хотя бы одну цифру')
#     if not re.search(r'\W', value):
#         raise ValueError('Пароль должен содержать хотя бы один специальный символ')
#     return value

# @validator('sex')
# def validate_sex(cls, value):
#     if value not in ["Мужской", "Женский"]:
#         raise ValueError("Пол должен быть в виде Мужской | Женский ")
#     return value

# @validator("phone")
# def validate_phone(cls, value):
#     if value and not re.match(r'^\+\d{1,15}$', value):
#         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
#     return value