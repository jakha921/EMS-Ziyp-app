from fastapi import APIRouter, Depends

from events.services import EventServices
from events.schemas import SEventCreate, SEventUpdate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/events",
    tags=["События"],
)


# CRUD
@router.get("", summary="Получить все события")
async def get_all_events(user: Users = Depends(get_current_user)):
    return await EventServices.find_all()


@router.get("/{event_id}", summary="Получить событие по id")
async def get_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await EventServices.find_one_or_none(id=event_id)


@router.post("", summary="Создать событие")
async def create_event(event: SEventCreate, user: Users = Depends(get_current_user)):
    return await EventServices.create(**event.dict())


@router.patch("/{event_id}", summary="Обновить событие по id")
async def update_event_by_id(event_id: int, event: SEventUpdate, user: Users = Depends(get_current_user)):
    return await EventServices.update(id=event_id, **event.dict())


@router.delete("/{event_id}", summary="Удалить событие по id")
async def delete_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await EventServices.delete(id=event_id)
# endregion