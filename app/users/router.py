from fastapi import APIRouter, Depends, HTTPException
from app.users.dao import UserDAO
from app.users.rb import RBUser
from app.users.schemas import User as SUser
from app.users.schemas import UserAdd as SUserAdd
from app.users.schemas import UpdateFilter, UserUpdate, DeleteFilter

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


@router.get("/", summary="Получить всех студентов")
async def get_all_users(request_body: RBUser = Depends()) -> list[SUser]:
    return await UserDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить пользователя через ID")
async def get_user_by_id(id: int) -> SUser | dict:
    result = await UserDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Пользователь по данному ID не найден.'}
    return result

@router.post("/add", summary="Добавить пользователя")
async def register_user(id: SUserAdd) -> dict:
    check = await UserDAO.add(**id.dict())
    if check:
        return {"message": "Новый пользователь добавлен.", "id": id}
    else:
        return {"message": "Пользователя не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить пользователя по ID")
async def update_user_handler(id: int, new_data: UserUpdate):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
    
    check = await UserDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о пользователе успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о пользователе.")
    
@router.delete("/delete/{id}", summary="Удалить пользователя по ID")
async def delete_user_handler(id: int):
    check = await UserDAO.delete(id=id)
    if check:
        return {"message": "Пользователь успешно удалён."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении пользователя.")