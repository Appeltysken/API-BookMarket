from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.reviews.dao import ReviewDAO
from app.entities.reviews.rb import RBReview
from app.entities.users.schemas import User as SUser
from app.entities.reviews.schemas import Review as SReview, ReviewAdd as SReviewAdd
from app.entities.reviews.schemas import ReviewUpdate
from app.entities.users.dependencies import get_current_user

router = APIRouter(prefix='/reviews', tags=['Работа с отзывами'])


@router.get("/", summary="Получить все отзывы")
async def get_all_reviews(request_body: RBReview = Depends(), current_user: SUser = Depends(get_current_user)) -> list[SReview]:
    if current_user.role_id == 2:
        return await ReviewDAO.find_all(**request_body.to_dict())
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

@router.get("/{id}", summary="Получить отзыв через ID")
async def get_reviews_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> SReview | dict:
    if current_user.role_id == 2 or current_user.id == id:
        result = await ReviewDAO.find_one_or_none_by_id(id)
        if result is None:
            return {'message': f'Книги по данному ID не найдено.'}
        return result
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

@router.post("/add", summary="Добавить отзыв")
async def add_review(review: SReviewAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    if current_user.role_id == 2 or current_user.id == id:
        review_dict = review.dict()
        review_dict['user_id'] = current_user.id
        check = await ReviewDAO.add(**review_dict)
        if check:
            return {"message": "Новая книга добавлена.", "review": review}
        else:
            return {"message": "Книгу не удалось добавить."}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.put("/update/{id}", summary="Обновить книгу по ID")
async def update_review_handler(id: int, new_data: ReviewUpdate, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        update_data = new_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
        check = await ReviewDAO.update(id=id, update_data=update_data)
        if check:
            return {"message": "Информация о книге успешно обновлена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о книге.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.delete("/delete/{id}", summary="Удалить книгу по ID")
async def delete_review_handler(id: int, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        check = await ReviewDAO.delete(id=id)
        if check:
            return {"message": "Книга успешно удалена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении книги.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")