from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
    
class Author(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="ФИО автора")
    bio: str = Field(None, max_length=500, description="Биография автора")
    author_picture: Optional[str] = Field(None, description="Название изображения автора")
    
class AuthorAdd(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="ФИО автора")
    bio: str = Field(None, max_length=500, description="Биография автора")
    
class UpdateFilter(BaseModel):
    id: int

class AuthorUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="ФИО автора")
    bio: str = Field(None, max_length=500, description="Биография автора")
    
class DeleteFilter(BaseModel):
    id: int
    
class AuthorPhoto(BaseModel):
    id: int
    author_picture: str = Field(None, description="Название изображения автора")