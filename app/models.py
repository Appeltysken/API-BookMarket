from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import Optional
import re



class Gender(str, Enum):
    male = "Мужской"
    female = "Женский"

class User(BaseModel):
    id: int
    username: str = Field(default=..., description="Логин пользователя, которым выступает номер телефона/адрес эл. почты")
    password: str = Field(default=..., min_length=8, description="Пароль пользователя, минимальная длина - 8 символов")
    Fname: str = Field(default=..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    Lname: date = Field(default=..., min_length=1, max_length=50, description="Фамилия пользователя, от 1 до 50 символов")
    sex: str = Field(default=..., description="Пол пользователя")
    email: EmailStr = Field(default=..., description="Электронная почта пользователя")
    phone: str = Field(default=..., description="Номер телефона пользователя")
    sell_history: str = Field(default=..., description="История продаж")
    buy_history: str = Field(default=..., description="История покупок")

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        phone = re.sub(r'\D', '', value)
        
        if len(phone) == 11 and phone.startswith("8"):
            return "7" + phone[1:]

        elif len(phone) == 11 and phone.startswith("7"):
            return phone

        elif re.match(r'^\S+@\S+\.\S+$', value):
            return value
        
        else:
            raise ValueError("Username должен быть номером телефона или адресом эл. почты")
    
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        
        if not re.search(r'[A-Za-z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        
        if not re.search(r'\W', value):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')
        
        return value
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, values: str) -> str:
        
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        
        return values