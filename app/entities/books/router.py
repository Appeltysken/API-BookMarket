from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.entities.books.dao import BookDAO
from app.entities.books.rb import RBBook
from app.entities.users.schemas import User as SUser
from app.entities.books.schemas import Book as SBook, BookAdd as SBookAdd
from app.entities.books.schemas import BookUpdate
from app.entities.users.dependencies import get_current_user
from app.entities.users.schemas import UserPhoto

router = APIRouter(prefix='/books', tags=['Работа с книгами'])


@router.get("/", summary="Получить все книги")
async def get_all_books(request_body: RBBook = Depends()) -> list[SBook]:
    return await BookDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить книгу через ID")
async def get_book_by_id(id: int) -> SBook | dict:
    result = await BookDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Книги по данному ID не найдено.'}
    return result

@router.post("/add", summary="Добавить книгу")
async def add_book(book: SBookAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    if current_user.role_id == 2 or current_user.id == id:
        book_dict = book.dict()
        book_dict['user_id'] = current_user.id
        check = await BookDAO.add(**book_dict)
        if check:
            return {"message": "Новая книга добавлена.", "book": book}
        else:
            return {"message": "Книгу не удалось добавить."}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.put("/update/{id}", summary="Обновить книгу по ID")
async def update_book_handler(id: int, new_data: BookUpdate, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        update_data = new_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
        check = await BookDAO.update(id=id, update_data=update_data)
        if check:
            return {"message": "Информация о книге успешно обновлена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о книге.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.delete("/delete/{id}", summary="Удалить книгу по ID")
async def delete_book_handler(id: int, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        check = await BookDAO.delete(id=id)
        if check:
            return {"message": "Книга успешно удалена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении книги.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

@router.post("/profile_picture/{id}", summary="Загрузить изображение книги")
async def upload_book_picture(id: int, book_picture: UploadFile = File(...), current_user: UserPhoto = Depends(get_current_user)):
    if current_user.id == id or current_user.role_id == 2:
        picture = await BookDAO.upload_image(entity_name="books", entity_id=id, file=book_picture, image_field="book_picture")
        return picture

@router.get("/profile_picture/{id}", summary="Получить изображение книги")
async def get_book_picture(id: int):
    picture = await BookDAO.get_image(entity_name="books", entity_id=id, image_field="book_picture")
    return picture

@router.delete("/profile_picture/{id}", summary="Удалить изображение книги")
async def delete_book_picture(id: int, current_user: UserPhoto = Depends(get_current_user)):
    if current_user.id == id or current_user.role_id == 2:
        picture = await BookDAO.delete_image(entity_name="books", entity_id=id, image_field="book_picture")
        return picture