from fastapi import APIRouter, Depends

from faqs.services import FAQsServices
from faqs.schemas import SFaqCreate, SFaqUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/faqs",
    tags=["FAQs"],
)


# CRUD
@router.get("", summary="Получить все FAQs")
async def get_all_faqs(user: Users = Depends(get_current_user), page: int = None, limit: int = None, search: str = None):
    return await FAQsServices.find_all(limit=limit, offset=page, search=search)


@router.get("/{faq_id}", summary="Получить FAQ по id")
async def get_faq_by_id(faq_id: int, user: Users = Depends(get_current_user)):
    return await FAQsServices.find_one_or_none(id=faq_id)


@router.post("", summary="Создать FAQ")
async def create_faq(faq: SFaqCreate, user: Users = Depends(get_current_user)):
    return await FAQsServices.create(**faq.dict())


@router.patch("/{faq_id}", summary="Обновить FAQ по id")
async def update_faq_by_id(faq_id: int, faq: SFaqUpdate, user: Users = Depends(get_current_user)):
    return await FAQsServices.update(id=faq_id, **faq.dict())


@router.delete("/{faq_id}", summary="Удалить FAQ по id")
async def delete_faq_by_id(faq_id: int, user: Users = Depends(get_current_user)):
    return await FAQsServices.delete(id=faq_id)
# endregion
