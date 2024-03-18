from fastapi import APIRouter, Depends

from application_grands.services import ApplicationGrandsServices
from application_grands.schemas import SApplicationGrandCreate, SApplicationGrandUpdate
from exeptions import AlreadyExistsException
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/applications/grands",
    tags=["Заявки на гранты"],
)


# CRUD
@router.get("", summary="Получить все заявки на гранты")
async def get_all_grands(user: Users = Depends(get_current_user),
                         page: int = None,
                         limit: int = None,
                         user_id: int = None,
                         grand_id: int = None,
                         status: str = None,
                         ):
    return await ApplicationGrandsServices.find_all(limit=limit, offset=page, user_id=user_id, grand_id=grand_id,
                                                    status=status)


@router.get("/{grand_id}", summary="Получить заявку на грант по id")
async def get_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await ApplicationGrandsServices.find_one_or_none(id=grand_id)


@router.post("", summary="Создать заявку на грант")
async def create_grand(grand: SApplicationGrandCreate, user: Users = Depends(get_current_user)):
    is_user_exist = await ApplicationGrandsServices.find_one_or_none(user_id=grand.user_id, grand_id=grand.grand_id)
    if is_user_exist:
        raise AlreadyExistsException("User already send application for grand")

    return await ApplicationGrandsServices.create(**grand.dict())


@router.patch("/{grand_id}", summary="Обновить заявку на грант по id")
async def update_grand_by_id(grand_id: int, grand: SApplicationGrandUpdate, user: Users = Depends(get_current_user)):
    return await ApplicationGrandsServices.update(id=grand_id, **grand.dict())


@router.delete("/{grand_id}", summary="Удалить заявку на грант по id")
async def delete_grand_by_id(grand_id: int, user: Users = Depends(get_current_user)):
    return await ApplicationGrandsServices.delete(id=grand_id)
