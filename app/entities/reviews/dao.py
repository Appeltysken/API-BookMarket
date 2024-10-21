from fastapi import APIRouter
from app.service.base import BaseDAO
from app.entities.reviews.models import Review

router = APIRouter(prefix='/reviews', tags=['Отзывы'])

class ReviewDAO(BaseDAO):
    model = Review