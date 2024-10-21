from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.orders.models import Book

router = APIRouter(prefix='/books', tags=['Книги'])

class BookDAO(BaseDAO):
    model = Book