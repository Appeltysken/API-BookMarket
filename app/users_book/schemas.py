import re
from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    username: str = Field(..., description="Username должен быть номером телефона или адресом эл. почты")
    Fname: str = Field(..., description="Имя пользователя")
    Lname: str = Field(..., description="Фамилия пользователя")
    sex: str = Field(..., description="Пол пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    phone: str = Field(None, description="Номер телефона пользователя")

class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя")

    @validator('username')
    def validate_username(cls, value):
        if not (re.match(r'^\S+@\S+\.\S+$', value) or re.match(r'^\d{11}$', value)):
            raise ValueError("Username должен быть номером телефона или адресом эл. почты")
        return value

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r'[A-Za-z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'\W', value):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')
        return value

    @validator('sex')
    def validate_sex(cls, value):
        if value not in ["Мужской", "Женский"]:
            raise ValueError("Пол должен быть в виде Мужской | Женский ")
        return value

    @validator("phone")
    def validate_phone(cls, value):
        if value and not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

class User(UserBase):
    id: int

    class Config:
        orm_mode = True