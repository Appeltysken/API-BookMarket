from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.entities.authors.dao import AuthorDAO
from app.entities.authors.rb import RBAuthor
from app.entities.users.schemas import User as SUser
from app.entities.authors.schemas import Author as SAuthor, AuthorAdd as SAuthorAdd, AuthorPhoto
from app.entities.authors.schemas import AuthorUpdate
from app.entities.users.dependencies import get_current_user
from app.entities.roles.permissions import permissions

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
@permissions("admin")
async def add_author(author: SAuthorAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    check = await AuthorDAO.add(**author.dict())
    if check:
        return {"message": "Новый автор добавлен.", "author": author}
    else:
        return {"message": "Автора не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить автора по ID")
@permissions("admin")
async def update_author_handler(id: int, new_data: AuthorUpdate, current_user: SUser = Depends(get_current_user)):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
    
    check = await AuthorDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация об авторе успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации об авторе.")
    
@router.delete("/delete/{id}", summary="Удалить автора по ID")
@permissions("admin")
async def delete_author_handler(id: int, current_user: SUser = Depends(get_current_user)):
    check = await AuthorDAO.delete(id=id)
    if check:
        return {"message": "Автор успешно удалён."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении автора.")

@router.post("/profile_picture/{id}", summary="Загрузить изображение профиля автора")
@permissions("admin")
async def upload_author_picture(id: int, author_picture: UploadFile = File(...), current_user: SUser = Depends(get_current_user)):
    picture = await AuthorDAO.upload_image(entity_name="authors", entity_id=id, file=author_picture, image_field="author_picture")
    return picture

@router.get("/profile_picture/{id}", summary="Получить изображение автора")
async def get_author_picture(id: int):
    picture = await AuthorDAO.get_image(entity_name="authors", entity_id=id, image_field="author_picture")
    return picture

@router.delete("/profile_picture/{id}", summary="Удалить изображение автора")
@permissions("admin")
async def delete_author_picture(id: int, current_user: SUser = Depends(get_current_user)):
    picture = await AuthorDAO.delete_image(entity_name="authors", entity_id=id, image_field="author_picture")
    return picture