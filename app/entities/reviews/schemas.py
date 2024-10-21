from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional

class Review(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: Optional[str] = Field(None, description="Текст комментария")
    mark: int = Field(..., description="Оценка книги (от 1 до 5)")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит отзыв")
    book_id: int = Field(..., description="ID книги, на которую оставлен отзыв")
    
    @validator('mark')
    @classmethod
    def validate_price(cls, value):
        if 1 <= value <= 5:
            raise ValueError('Оценка должна лежать в диапозоне от 1 до 5.')
        return value
    
class ReviewAdd(BaseModel):
    text: Optional[str] = Field(None, description="Статус заказа")
    mark: int = Field(..., description="Статус заказа")
    book_id: int = Field(..., description="ID книги, на которую оставлен отзыв")
    
    @validator('mark')
    @classmethod
    def validate_price(cls, value):
        if 1 <= value <= 5:
            raise ValueError('Оценка должна лежать в диапозоне от 1 до 5.')
        return value
    
class UpdateFilter(BaseModel):
    id: int

class ReviewUpdate(BaseModel):
    text: Optional[str] = Field(None, description="Текст комментария")
    mark: int = Field(..., description="Оценка книги (от 1 до 5)")
    
    @validator('mark')
    @classmethod
    def validate_price(cls, value):
        if 1 <= value <= 5:
            raise ValueError('Оценка должна лежать в диапозоне от 1 до 5.')
        return value
    
class DeleteFilter(BaseModel):
    id: int