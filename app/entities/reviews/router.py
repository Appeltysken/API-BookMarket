from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.reviews.dao import ReviewDAO
from app.entities.reviews.rb import RBReview
from app.entities.users.schemas import User as SUser
from app.entities.reviews.schemas import Review as SReview, ReviewAdd as SReviewAdd
from app.entities.reviews.schemas import ReviewUpdate
from app.entities.users.dependencies import get_current_user
from app.entities.books.dao import BookDAO
from app.entities.roles.permissions import permissions

router = APIRouter(prefix='/reviews', tags=['Работа с отзывами'])


@router.get("/", summary="Получить все отзывы")
async def get_all_reviews(request_body: RBReview = Depends()) -> list[SReview]:
    return await ReviewDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить отзыв через ID")
async def get_reviews_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> SReview | dict:
    result = await ReviewDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Отзыва по данному ID не найдено.'}
    return result

@router.post("/add", summary="Добавить отзыв")
@permissions()
async def add_review(review: SReviewAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    book = await BookDAO.find_one_or_none_by_id(review.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    review_dict = review.dict()
    review_dict['user_id'] = current_user.id
    check = await ReviewDAO.add(**review_dict)
        
    if book.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нельзя оставлять отзыв на собственную книгу")
        
    if check:
        return {"message": "Новый отзыв добавлен.", "review": review}
    else:
        return {"message": "Отзыв не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить отзыв по ID")
@permissions("self_or_admin")
async def update_review_handler(id: int, new_data: ReviewUpdate, current_user: SUser = Depends(get_current_user)):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
    check = await ReviewDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация об отзыве успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации об отзыве.")

@router.delete("/delete/{id}", summary="Удалить отзыв по ID")
@permissions("self_or_admin")
async def delete_review_handler(id: int, current_user: SUser = Depends(get_current_user)):
    check = await ReviewDAO.delete(id=id)
    if check:
        return {"message": "Отзыв успешно удален."}
    else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении отзыва.")