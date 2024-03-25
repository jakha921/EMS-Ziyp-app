from fastapi import APIRouter, Depends

from application_events.services import ApplicationEventServices
from application_events.schemas import SApplicationEventCreate, SSApplicationEventUpdate
from exeptions import AlreadyExistsException
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/applications/events",
    tags=["Заявки на события"],
)


# CRUD
@router.get("", summary="Получить все заявки на события")
async def get_all_events(user: Users = Depends(get_current_user),
                         page: int = None,
                         limit: int = None,
                         user_id: int = None,
                         event_id: int = None,
                         status: str = None,  # approved, rejected, pending
                         ):
    return await ApplicationEventServices.find_all(page=page, limit=limit, user_id=user_id, event_id=event_id,
                                                   status=status)


@router.get("/{event_id}", summary="Получить заявку на событие по id")
async def get_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await ApplicationEventServices.find_one_or_none(id=event_id)


@router.post("", summary="Создать заявку на событие")
async def create_event(event: SApplicationEventCreate, user: Users = Depends(get_current_user), lang: str = "ru"):
    is_event_exist = await ApplicationEventServices.find_one_or_none(user_id=event.user_id, event_id=event.event_id)
    if is_event_exist:
        raise AlreadyExistsException("User already send application for event")

    return await ApplicationEventServices.create(**event.dict(), lang=lang)


@router.patch("/{event_id}", summary="Обновить заявку на событие по id")
async def update_event_by_id(event_id: int, event: SSApplicationEventUpdate, user: Users = Depends(get_current_user),
                             lang: str = "ru"):
    return await ApplicationEventServices.update(id=event_id, **event.dict(), lang=lang)


@router.delete("/{event_id}", summary="Удалить заявку на событие по id")
async def delete_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await ApplicationEventServices.delete(id=event_id)
# endregion
