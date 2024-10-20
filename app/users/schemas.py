import re
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional
from fastapi import UploadFile, File

class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., description="Username должен быть номером телефона или адресом эл. почты")
    password: str = Field(..., min_lenght=8, description="Пароль пользователя")
    Fname: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя пользователя")
    Lname: Optional[str] = Field(None, min_length=1, max_length=50, description="Фамилия пользователя")
    sex: Optional[str] = Field(None, description="Пол пользователя")
    email: Optional[EmailStr] = Field(None, description="Электронная почта пользователя")
    phone: Optional[str] = Field(None, description="Номер телефона пользователя")
    sell_history: Optional[str] = Field(None, description="История продаж")
    buy_history: Optional[str] = Field(None, description="История покупок")
    
    @validator('username')
    @classmethod
    def validate_username(cls, value):
        if not (re.match(r'^\S+@\S+\.\S+$', value) or re.match(r'^\d{11}$', value)):
            raise ValueError("Username должен быть номером телефона или адресом эл. почты")
        return value

    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.search(r'[A-Za-z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'\W', value):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')
        return value

    @validator('sex')
    @classmethod
    def validate_sex(cls, value):
        if value and value not in ["Мужской", "Женский"]:
            raise ValueError("Пол должен быть в виде Мужской | Женский ")
        return value

    @validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value and not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

class User(BaseUser):
    id: int
    role_id: int = Field(None, description="Роль пользователя")
    
    class Config:
        orm_mode = True
        
class UpdateFilter(BaseModel):
    id: int

class UserUpdate(BaseUser):
    username: Optional[str] = Field(None, description="Username должен быть номером телефона или адресом эл. почты")
    password: Optional[str] = Field(None, min_lenght=8, description="Пароль пользователя") 

class DeleteFilter(BaseModel):
    id: int
    
class UserAuth(BaseModel):
    username: str = Field(..., description="Username должен быть номером телефона или адресом эл. почты")
    password: str = Field(..., min_lenght=8, description="Пароль пользователя")
    
class UserPhoto(BaseModel):
    profile_picture: Optional[str] = Field(None, description="Название изображения")