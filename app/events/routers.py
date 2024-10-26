import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from events.schemas import SEventCreate, SEventUpdate
from events.services import EventServices
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/events",
    tags=["События"],
)


# CRUD
@router.get("", summary="Получить все события")
async def get_all_events(
        new_event: bool = None,
        is_paid_event: bool = None,
        page: int = None,
        limit: int = None,
        search: str = None,
        date_now: date = datetime.date.today()
):
    return await EventServices.find_all(new_event=new_event,
                                        is_paid_event=is_paid_event,
                                        limit=limit,
                                        offset=page,
                                        search=search,
                                        date_now=date_now
                                        )


@router.get("/{event_id}", summary="Получить событие по id")
async def get_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await EventServices.find_one_or_none(id=event_id)


@router.post("", summary="Создать событие")
async def create_event(event: SEventCreate, user: Users = Depends(get_current_user)):
    try:
        if event.start_date < date.today():
            raise ValueError("Дата начала события не может быть раньше сегодняшней даты")
        return await EventServices.create(**event.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "detail": f"{e}",
            "data": None
        }
                            )
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "detail": f"Ошибка при создании события: {e}",
            "data": None
        }
                            )


@router.patch("/{event_id}", summary="Обновить событие по id")
async def update_event_by_id(event_id: int, event: SEventUpdate, user: Users = Depends(get_current_user)):
    return await EventServices.update(id=event_id, **event.dict())


@router.delete("/{event_id}", summary="Удалить событие по id")
async def delete_event_by_id(event_id: int, user: Users = Depends(get_current_user)):
    return await EventServices.delete(id=event_id)
# endregion
