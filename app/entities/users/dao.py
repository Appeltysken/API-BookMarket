from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.users.models import User

router = APIRouter(prefix='/users', tags=['Пользователи'])

class UserDAO(BaseDAO):
    model = User