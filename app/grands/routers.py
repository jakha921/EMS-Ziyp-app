from fastapi import APIRouter, Depends

from grands.schemas import SGrandCreate, SGrandUpdate
from grands.services import GrandsServices
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/grands",
    tags=["Гранды"],
)


# CRUD
@router.get("", summary="Получить все гранды")
async def get_all_grands(
        page: int = None,
        limit: int = None,
        search: str = None,
):
    return await GrandsServices.find_all(limit=limit, offset=page, search=search)


@router.get("/{grand_id}", summary="Получить гранд по id")
async def get_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await GrandsServices.find_one_or_none(id=grand_id)


@router.post("", summary="Создать гранд")
async def create_grand(grand: SGrandCreate, user: Users = Depends(get_current_user)):
    return await GrandsServices.create(**grand.dict())


@router.patch("/{grand_id}", summary="Обновить гранд по id")
async def update_grand_by_id(grand_id: int, grand: SGrandUpdate, user: Users = Depends(get_current_user)):
    return await GrandsServices.update(id=grand_id, **grand.dict())


@router.delete("/{grand_id}", summary="Удалить гранд по id")
async def delete_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await GrandsServices.delete(id=grand_id)
# endregion
