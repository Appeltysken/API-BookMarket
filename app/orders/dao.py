from fastapi import APIRouter
from app.service.base import BaseDAO
from app.orders.models import Order

router = APIRouter(prefix='/orders', tags=['Заказы'])

class OrderDAO(BaseDAO):
    model = Order