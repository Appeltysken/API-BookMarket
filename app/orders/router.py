from fastapi import APIRouter, Depends, HTTPException
from app.orders.dao import OrderDAO
from app.orders.rb import RBOrder
from app.orders.schemas import Order as SOrder
from app.orders.schemas import OrderAdd as SOrderAdd
from app.orders.schemas import UpdateFilter, OrderUpdate, DeleteFilter

router = APIRouter(prefix='/orders', tags=['Работа с заказами'])


@router.get("/", summary="Получить все заказы")
async def get_all_orders(request_body: RBOrder = Depends()) -> list[SOrder]:
    return await OrderDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить заказ через ID")
async def get_order_by_id(id: int) -> SOrder | dict:
    result = await OrderDAO.find_one_or_none_by_id(id)
    if result is None:
        return {'message': f'Заказ по данному ID не найден.'}
    return result

# @router.get("/by_filter", summary="Получить заказ через параметр")
# async def get_order_by_filter(request_body: RBOrder = Depends()) -> SOrder | dict:
#    result = await OrderDAO.find_one_or_none(**request_body.to_dict())
#    if result is None:
#        return {'message': f'Заказ по данному параметру не найден.'}
#    return result

@router.post("/add", summary="Добавить заказ через ID")
async def register_user(order: SOrderAdd) -> dict:
    check = await OrderDAO.add(**order.dict())
    if check:
        return {"message": "Новый заказ добавлен.", "order": order}
    else:
        return {"message": "Заказ не удалось добавить."}
    
@router.put("/update", summary="Обновить заказ по ID")
async def update_user_handler(filter_order: UpdateFilter, new_data: OrderUpdate):
    update_data = new_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    check = await OrderDAO.update(filter_order.dict(), update_data)
    if check:
        return {"message": "Информация о заказе успешно обновлена."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о заказе.")
    
@router.delete("/delete", summary="Удалить заказ по ID")
async def delete_user_handler(filter_user: DeleteFilter):
    check = await OrderDAO.delete(**filter_user.dict())
    if check:
        return {"message": "Заказ успешно удалён."}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении заказа.")