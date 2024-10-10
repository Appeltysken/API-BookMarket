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

# @router.get("/by_filter", summary="Получить пользователя через параметр")
# async def get_user_by_filter(request_body: RBUser = Depends()) -> SUser | dict:
#    result = await UserDAO.find_one_or_none(**request_body.to_dict())
#    if result is None:
#        return {'message': f'Пользователь по данному параметру не найден.'}
#    return result

@router.post("/add", summary="Добавить пользователя через ID")
async def register_user(order: SUserAdd) -> dict:
    check = await UserDAO.add(**order.dict())
    if check:
        return {"message": "Новый заказ добавлен.", "order": order}
    else:
        return {"message": "Заказ не удалось добавить."}
    
@router.put("/update", summary="Обновить пользователя по ID")
async def update_user_handler(filter_order: UpdateFilter, new_data: UserUpdate):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    check = await UserDAO.update(filter_order.dict(), update_data)
    if check:
        return {"message": "Информация о пользователе успешно обновлена. "}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о пользователе.")
    
@router.delete("/delete", summary="Удалить пользователя по ID")
async def delete_user_handler(filter_user: DeleteFilter):
    check = await UserDAO.delete(**filter_user.dict())
    if check:
        return {"message": "Пользователь успешно удалён!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении пользователя.")