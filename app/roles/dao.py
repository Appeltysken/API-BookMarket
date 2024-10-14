from fastapi import APIRouter
from app.service.base import BaseDAO
from app.roles.models import Role

router = APIRouter(prefix='/roles', tags=['Роли'])

class RoleDAO(BaseDAO):
    model = Role