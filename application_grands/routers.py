from fastapi import APIRouter, Depends

from grands.services import GrandsServices
from grands.schemas import SGrandCreate, SGrandUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/applications/grands",
    tags=["Заявки на гранты"],
)


# CRUD
@router.get("", summary="Получить все заявки на гранты")
async def get_all_grands(user: Users = Depends(get_current_user)):
    return await GrandsServices.find_all()


@router.get("/{grand_id}", summary="Получить заявку на грант по id")
async def get_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await GrandsServices.find_one(id=grand_id)


@router.post("", summary="Создать заявку на грант")
async def create_grand(grand: SGrandCreate, user: Users = Depends(get_current_user)):
    return await GrandsServices.create(**grand.dict())


@router.patch("/{grand_id}", summary="Обновить заявку на грант по id")
async def update_grand_by_id(grand_id: int, grand: SGrandUpdate, user: Users = Depends(get_current_user)):
    return await GrandsServices.update(id=grand_id, **grand.dict())


@router.delete("/{grand_id}", summary="Удалить заявку на грант по id")
async def delete_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await GrandsServices.delete(id=grand_id)
