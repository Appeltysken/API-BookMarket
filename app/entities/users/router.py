from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File
from app.entities.users.dao import UserDAO
from app.entities.users.auth import get_password_hash, authenticate_user, create_access_token
from app.entities.users.schemas import User as SUser
from app.entities.users.rb import RBUser
from app.entities.users.schemas import BaseUser, UserAuth, UserUpdate, UserPhoto
from app.entities.users.dependencies import get_current_user
from app.entities.roles.permissions import permissions
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

UPLOAD_FOLDER = "uploads/"

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей")
@permissions("admin")
async def get_all_users(request_body: RBUser = Depends(), current_user: SUser = Depends(get_current_user)) -> list[SUser]:
    return await UserDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить пользователя через ID")
@permissions("self_or_admin")
async def get_user_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> SUser | dict:
    result = await UserDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Пользователь по данному ID не найден.'}
    return result

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: BaseUser) -> dict:
    user = await UserDAO.find_one_or_none(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким username уже существует"
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    
    return {"message": "Вы успешно зарегистрированы!"}

@router.post("/login/", summary="Логин пользователя")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token)
    
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/", summary="Получить данные текущего пользователя")
async def get_me(user_data: SUser = Depends(get_current_user)):
    return user_data

@router.post("/logout/", summary="Выйти из системы")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.put("/update/{id}", summary="Обновить пользователя по ID")
@permissions("self_or_admin")
async def update_user_handler(id: int, new_data: UserUpdate, current_user: SUser = Depends(get_current_user)):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
    check = await UserDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о пользователе успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о пользователе.")

@router.delete("/delete/{id}", summary="Удалить пользователя по ID")
@permissions("self_or_admin")
async def delete_user_handler(id: int, current_user: SUser = Depends(get_current_user)):
    check = await UserDAO.delete(id=id)
    if check:
        return {"message": "Пользователь успешно удалён."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении пользователя.")

@router.post("/profile_picture/{id}", summary="Загрузить изображение профиля пользователя")
@permissions("self_or_admin")
async def upload_profile_picture(id: int, profile_picture: UploadFile = File(...), current_user: UserPhoto = Depends(get_current_user)):
    picture = await UserDAO.upload_image(entity_name="users", entity_id=id, file=profile_picture, image_field="profile_picture")
    return picture

@router.get("/profile_picture/{id}", summary="Получить изображение профиля")
@permissions("self_or_admin")
async def get_profile_picture(id: int, current_user: UserPhoto = Depends(get_current_user)):
    picture = await UserDAO.get_image(entity_name="users", entity_id=id, image_field="profile_picture")
    return picture

@router.delete("/profile_picture/{id}", summary="Удалить изображение профиля")
@permissions("self_or_admin")
async def delete_profile_picture(id: int, current_user: UserPhoto = Depends(get_current_user)):
    picture = await UserDAO.delete_image(entity_name="users", entity_id=id, image_field="profile_picture")
    return picture