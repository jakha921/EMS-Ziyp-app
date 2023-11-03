from fastapi import APIRouter, Response, Depends, Request

from exeptions import UserAlreadyExistsWithThisEmailException, UserNotFoundException
from users.auth import hash_password, authenticate_user, create_access_token
from users.dependencies import get_current_user, get_current_is_admin
from users.models import Users
from users.services import UserServices
from users.schemas import SUserRegister, SUserAuth, SAdminRegister, SAdminAuth

router = APIRouter()


# region Master and Admin

@router.post("/admin/register", tags=["Мастера и Администраторы"], summary="Регистрация администратора")
@router.post("/master/register", tags=["Мастера и Администраторы"], summary="Регистрация мастера")
async def register_user(user: SAdminRegister, request: Request):
    is_user_exist = await UserServices.find_one_or_none(email=user.email)

    if is_user_exist:
        raise UserAlreadyExistsWithThisEmailException

    hashed_password = hash_password(user.password)

    if request.url.path == "/admin/register":
        return await UserServices.create(email=user.email, hashed_password=hashed_password, role="admin")
    else:
        return await UserServices.create(email=user.email, hashed_password=hashed_password, role="master")


@router.post("/login", tags=["Мастера и Администраторы"], summary="Авторизация администратора или мастера")
async def login_user(response: Response, user: SAdminAuth):
    user = await authenticate_user(email=user.email, password=user.password)
    if not user:
        raise UserNotFoundException

    # create access token
    token = create_access_token({"sub": str(user.id)})

    # set cookie
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout", tags=["Мастера и Администраторы"], summary="Выход администратора или мастера")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


# endregion

# region Auth & Users
@router.post("/user/register", tags=["Auth & Пользователи"], summary="Регистрация пользователя")
async def register_user(user: SUserRegister):
    is_user_exist = await UserServices.find_one_or_none(phone=user.phone)

    if is_user_exist:
        raise UserAlreadyExistsWithThisEmailException

    hashed_password = hash_password(user.password)
    return await UserServices.create(phone=user.phone, hashed_password=hashed_password, role="user")


@router.post("/user/login", tags=["Auth & Пользователи"], summary="Авторизация пользователя")
async def login_user(response: Response, user: SUserAuth):
    user = await authenticate_user(phone=user.phone, password=user.password)
    if not user:
        raise UserNotFoundException

    # create access token
    token = create_access_token({"sub": str(user.id)})

    # set cookie
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/user/logout", tags=["Auth & Пользователи"], summary="Выход пользователя")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/user/me", tags=["Auth & Пользователи"], summary="Получить данные текущего пользователя")
async def get_me(user: Users = Depends(get_current_user)):
    return user


@router.get("/user/all", tags=["Auth & Пользователи"], summary="Получить всех пользователей")
async def get_all_users(user: Users = Depends(get_current_is_admin)):
    return await UserServices.find_all()
# endregion
