from fastapi import APIRouter, Depends

from products.services import ProductService
from products.schemas import SProductCreate, SProductUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/products",
    tags=["Продукты"],
)


# CRUD
@router.get("", summary="Получить все продукты")
async def get_all_products(user: Users = Depends(get_current_user),
                           page: int = None,
                           limit: int = None,
                           search: str = None,
                           category_id: int = None,
                           ):
    return await ProductService.find_all(limit=limit, offset=page, search=search, category_id=category_id)


@router.get("/{product_id}", summary="Получить продукт по id")
async def get_product_by_id(product_id: int, user: Users = Depends(get_current_user)):
    return await ProductService.find_one_or_none(id=product_id)


@router.post("", summary="Создать продукт")
async def create_product(product: SProductCreate, user: Users = Depends(get_current_user)):
    return await ProductService.create(**product.dict())


@router.patch("/{product_id}", summary="Обновить продукт по id")
async def update_product_by_id(product_id: int, product: SProductUpdate, user: Users = Depends(get_current_user)):
    return await ProductService.update(id=product_id, **product.dict())


@router.delete("/{product_id}", summary="Удалить продукт по id")
async def delete_product_by_id(product_id: int, user: Users = Depends(get_current_user)):
    return await ProductService.delete(id=product_id)
# endregion
