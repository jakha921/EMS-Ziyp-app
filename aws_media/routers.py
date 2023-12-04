from fastapi import APIRouter, Depends, UploadFile, File

from aws_media.services import upload_file
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter()


@router.post("/upload/media", summary="Загрузить файл")
async def upload_complain_file(file: UploadFile = File(...),
                               user: Users = Depends(get_current_user)):
    return await upload_file(file)

# endregion
