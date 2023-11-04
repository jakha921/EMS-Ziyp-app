from fastapi import APIRouter, Depends

from orders.services import OrderServices
from orders.schemas import SOrderCreate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


# CRUD
@router.get("", summary="Получить все заказы")
async def get_all_orders(user: Users = Depends(get_current_user)):
    return await OrderServices.find_all()


@router.get("/{order_id}", summary="Получить заказ по id")
async def get_order_by_id(order_id: int, user: Users = Depends(get_current_user)):
    return await OrderServices.find_one_or_none(id=order_id)


@router.post("", summary="Создать заказ")
async def create_order(order: SOrderCreate, user: Users = Depends(get_current_user)):
    return await OrderServices.create(**order.dict())


@router.patch("/{order_id}", summary="Обновить заказ по id")
async def update_order_by_id(order_id: int, order: SOrderCreate, user: Users = Depends(get_current_user)):
    return await OrderServices.update(id=order_id, **order.dict())


@router.delete("/{order_id}", summary="Удалить заказ по id")
async def delete_order_by_id(order_id: int, user: Users = Depends(get_current_user)):
    return await OrderServices.delete(id=order_id)
# endregion
