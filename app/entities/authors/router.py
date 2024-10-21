from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.entities.authors.dao import AuthorDAO
from app.entities.authors.rb import RBAuthor
from app.entities.users.schemas import User as SUser
from app.entities.authors.schemas import Author as SAuthor, AuthorAdd as SAuthorAdd, AuthorPhoto
from app.entities.authors.schemas import AuthorUpdate
from app.entities.users.dependencies import get_current_user

router = APIRouter(prefix='/authors', tags=['Работа с авторами'])


@router.get("/", summary="Получить всех авторов")
async def get_all_authors(request_body: RBAuthor = Depends()) -> list[SAuthor]:
    return await AuthorDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить автора через ID")
async def get_author_by_id(id: int) -> SAuthor | dict:
    result = await AuthorDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Автора по данному ID не найдено.'}
    return result

@router.post("/add", summary="Добавить автора")
async def register_user(author: SAuthorAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    if current_user.role_id == 2:
        check = await AuthorDAO.add(**author.dict())
        if check:
            return {"message": "Новый автор добавлен.", "author": author}
        else:
            return {"message": "Автора не удалось добавить."}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.put("/update/{id}", summary="Обновить автора по ID")
async def update_user_handler(id: int, new_data: AuthorUpdate, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2:
        update_data = new_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
        check = await AuthorDAO.update(id=id, update_data=update_data)
        if check:
            return {"message": "Информация об авторе успешно обновлена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при обновлении информации об авторе.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    
@router.delete("/delete/{id}", summary="Удалить автора по ID")
async def delete_user_handler(id: int, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2:
        check = await AuthorDAO.delete(id=id)
        if check:
            return {"message": "Автор успешно удалён."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении автора.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

@router.post("/profile_picture/{id}", summary="Загрузить изображение профиля автора")
async def upload_profile_picture(id: int, author_picture: UploadFile = File(...), current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2:
        picture = await AuthorDAO.upload_image(entity_name="authors", entity_id=id, file=author_picture, image_field="author_picture")
        return picture

@router.get("/profile_picture/{id}", summary="Получить изображение автора")
async def get_profile_picture(id: int):
    picture = await AuthorDAO.get_image(entity_name="authors", entity_id=id, image_field="author_picture")
    return picture

@router.delete("/profile_picture/{id}", summary="Удалить изображение автора")
async def delete_profile_picture(id: int, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2:
        picture = await AuthorDAO.delete_image(entity_name="authors", entity_id=id, image_field="author_picture")
        return picture