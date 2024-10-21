from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.authors.models import Author

router = APIRouter(prefix='/authors', tags=['Авторы'])

class AuthorDAO(BaseDAO):
    model = Author