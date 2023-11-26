from fastapi import APIRouter, Depends

from news.services import NewsServices
from news.schemas import SNewsCreate, SNewsUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/news",
    tags=["Новости"],
)


# CRUD
@router.get("", summary="Получить все новости")
async def get_all_news(user: Users = Depends(get_current_user),
                       limit: int = None,
                       offset: int = None,
                       search: str = None):
    return await NewsServices.find_all(limit=limit, offset=offset, search=search)


@router.get("/{news_id}", summary="Получить новость по id")
async def get_news_by_id(news_id: int, user: Users = Depends(get_current_user)):
    return await NewsServices.find_one(id=news_id)


@router.post("", summary="Создать новость")
async def create_news(news: SNewsCreate, user: Users = Depends(get_current_user)):
    return await NewsServices.create(**news.dict())


@router.patch("/{news_id}", summary="Обновить новость по id")
async def update_news_by_id(news_id: int, news: SNewsUpdate, user: Users = Depends(get_current_user)):
    return await NewsServices.update(id=news_id, **news.dict())


@router.delete("/{news_id}", summary="Удалить новость по id")
async def delete_news_by_id(news_id: int, user: Users = Depends(get_current_user)):
    return await NewsServices.delete(id=news_id)
# endregion
