from fastapi import APIRouter, Depends

from categories.services import CategoryServices
from categories.schemas import SCategoryCreate, SCategoryUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/categories",
    tags=["Категории"],
)


# CRUD
@router.get("", summary="Получить все категории")
async def get_all_categories(user: Users = Depends(get_current_user)):
    return await CategoryServices.find_all()


@router.get("/{category_id}", summary="Получить категорию по id")
async def get_category_by_id(category_id: int, user: Users = Depends(get_current_user)):
    return await CategoryServices.find_one_or_none(id=category_id)


@router.post("", summary="Создать категорию")
async def create_category(category: SCategoryCreate, user: Users = Depends(get_current_user)):
    return await CategoryServices.create(**category.dict())


@router.patch("/{category_id}", summary="Обновить категорию по id")
async def update_category_by_id(category_id: int, category: SCategoryUpdate, user: Users = Depends(get_current_user)):
    return await CategoryServices.update(id=category_id, **category.dict())


@router.delete("/{category_id}", summary="Удалить категорию по id")
async def delete_category_by_id(category_id: int, user: Users = Depends(get_current_user)):
    return await CategoryServices.delete(id=category_id)
# endregion
