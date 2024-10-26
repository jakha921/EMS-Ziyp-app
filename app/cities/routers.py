from fastapi import APIRouter, Depends

from cities.schemas import SCityCreate, SCityUpdate
from cities.services import CityServices
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/cities",
    tags=["Города"],
)


# CRUD
@router.get("", summary="Получить все города")
async def get_all_cities(
        page: int = None,
        limit: int = None,
):
    return await CityServices.find_all(limit=limit, offset=page)


@router.get("/{city_id}", summary="Получить город по id")
async def get_city_by_id(city_id: int, user: Users = Depends(get_current_user)):
    return await CityServices.find_one_or_none(id=city_id)


@router.post("", summary="Создать город")
async def create_city(city: SCityCreate):  # user: Users = Depends(get_current_user)
    return await CityServices.create(**city.dict())


@router.patch("/{city_id}", summary="Обновить город по id")
async def update_city_by_id(city_id: int, city: SCityUpdate, user: Users = Depends(get_current_user)):
    return await CityServices.update(id=city_id, **city.dict())


@router.delete("/{city_id}", summary="Удалить город по id")
async def delete_city_by_id(city_id: int, user: Users = Depends(get_current_user)):
    return await CityServices.delete(id=city_id)
# endregion
