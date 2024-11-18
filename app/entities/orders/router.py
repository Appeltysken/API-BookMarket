from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.orders.dao import OrderDAO
from app.entities.orders.rb import RBOrder
from app.entities.orders.schemas import Order as SOrder
from app.entities.orders.schemas import OrderAdd as SOrderAdd
from app.entities.orders.schemas import OrderUpdate
from app.entities.users.schemas import User as SUser
from app.entities.users.dependencies import get_current_user
from app.entities.roles.permissions import permissions

router = APIRouter(prefix='/orders', tags=['Работа с заказами'])

@router.get("/", summary="Получить все заказы")
@permissions("admin")
async def get_all_orders(request_body: RBOrder = Depends(), current_user: SUser = Depends(get_current_user)) -> list[SOrder]:
    return await OrderDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить заказ через ID")
@permissions("self_or_admin")
async def get_order_by_id(
    id: int, 
    current_user: SUser = Depends(get_current_user)) -> SOrder | dict:
    result = await OrderDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Заказ по данному ID не найден.'}
    return SOrder.from_orm(result)

@router.post("/add", summary="Добавить заказ")
@permissions()
async def add_order(order: SOrderAdd, current_user: SUser = Depends(get_current_user)) -> dict:
    check = await OrderDAO.add(**order.dict())
    if check:
        return {"message": "Новый заказ добавлен.", "order": order}
    else:
        return {"message": "Заказ не удалось добавить."}
    
@router.put("/update/{id}", summary="Обновить заказ по ID")
@permissions("self_or_admin")
async def update_user_handler(id: int, new_data: OrderUpdate, current_user: SUser = Depends(get_current_user)):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
        
    check = await OrderDAO.update(id=id, update_data=update_data)
    if check:
        return {"message": "Информация о заказе успешно обновлена."}
    else:
            raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о заказе.")
    
@router.delete("/delete/{id}", summary="Удалить заказ по ID")
@permissions("self_or_admin")
async def delete_user_handler(id: int, current_user: SUser = Depends(get_current_user)):
    check = await OrderDAO.delete(id=id)
    if check:
        return {"message": "Заказ успешно удалён."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении заказа.")