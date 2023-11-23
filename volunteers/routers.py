from fastapi import APIRouter, Depends

from volunteers.services import VolunteerServices
from volunteers.schemas import SVolunteerCreate
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/volunteers",
    tags=["Волонтеры"],
)


# CRUD
@router.get("", summary="Получить всех волонтеров")
async def get_all_volunteers(user: Users = Depends(get_current_user)):
    return await VolunteerServices.find_all()


@router.get("/{volunteer_id}", summary="Получить волонтера по id")
async def get_volunteer_by_id(volunteer_id: int, user: Users = Depends(get_current_user)):
    return await VolunteerServices.find_one_or_none(id=volunteer_id)


@router.post("", summary="Создать волонтера")
async def create_volunteer(volunteer: SVolunteerCreate, user: Users = Depends(get_current_user)):
    return await VolunteerServices.create(**volunteer.dict())


@router.patch("/{volunteer_id}", summary="Обновить волонтера по id")
async def update_volunteer_by_id(volunteer_id: int, volunteer: SVolunteerCreate,
                                 user: Users = Depends(get_current_user)):
    return await VolunteerServices.update(id=volunteer_id, **volunteer.dict())


@router.delete("/{volunteer_id}", summary="Удалить волонтера по id")
async def delete_volunteer_by_id(volunteer_id: int, user: Users = Depends(get_current_user)):
    return await VolunteerServices.delete(id=volunteer_id)

# endregion
