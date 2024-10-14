from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.users.dao import UserDAO
from app.users.rb import RBUser
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.schemas import User as SUser
from app.users.schemas import BaseUser, UserAuth, UserUpdate
from app.users.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей")
async def get_all_users(current_admin_user: SUser = Depends(get_current_admin_user)) -> list[SUser]:
    return await UserDAO.find_all()

@router.get("/{id}", summary="Получить пользователя через ID")
async def get_user_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> SUser | dict:
    if current_user.role_id == 2 or current_user.id == id:
        result = await UserDAO.find_one_or_none_by_id(id)
        if result is None:
            return {'message': f'Пользователь по данному ID не найден.'}
        return result
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: BaseUser) -> dict:
    user = await UserDAO.find_one_or_none(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким username уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/", summary="Получить данные текущего пользователя")
async def get_me(user_data: SUser = Depends(get_current_user)):
    return user_data

@router.post("/logout/", summary="Выйти из системы")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.put("/update/{id}", summary="Обновить пользователя по ID")
async def update_user_handler(id: int, new_data: UserUpdate, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        update_data = new_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
        check = await UserDAO.update(id=id, update_data=update_data)
        if check:
            return {"message": "Информация о пользователе успешно обновлена."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о пользователе.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа для обновления")

@router.delete("/delete/{id}", summary="Удалить пользователя по ID")
async def delete_user_handler(id: int, current_user: SUser = Depends(get_current_user)):
    if current_user.role_id == 2 or current_user.id == id:
        check = await UserDAO.delete(id=id)
        if check:
            return {"message": "Пользователь успешно удалён."}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при удалении пользователя.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа для удаления")