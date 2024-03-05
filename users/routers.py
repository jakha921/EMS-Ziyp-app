from fastapi import APIRouter, Response, Depends, Request

from exeptions import UserAlreadyExistsWithThisEmailException, UserNotFoundException, AlreadyExistsException
from users.auth import hash_password, authenticate_user, create_access_token
from users.dependencies import get_current_user, get_current_is_admin
from users.models import Users
from users.services import UserServices
from users.schemas import SUserRegister, SUserAuth, SAdminRegister, SAdminAuth, SUserUpdate, SMasterRester, \
    SUserSocialRegister, SUserSocialAuth

router = APIRouter()


# region Master and Admin

@router.post("/admin/register", tags=["Администраторы"], summary="Регистрация администратора")
async def register_user(user: SAdminRegister):
    is_user_exist = await UserServices.find_one_or_none(email=user.email)

    if is_user_exist:
        raise UserAlreadyExistsWithThisEmailException

    hashed_password = hash_password(user.password)

    user = {
        "email": user.email,
        "hashed_password": hashed_password,
        "role": "admin",
        "first_name": user.first_name if user.first_name else None,
        "last_name": user.last_name if user.last_name else None,
    }

    return await UserServices.create(**user)


@router.post("/admin/login", tags=["Администраторы"], summary="Авторизация администратора")
async def login_user(response: Response, user: SAdminAuth):
    user = await authenticate_user(email=user.email, password=user.password)
    if not user:
        raise UserNotFoundException

    # create access token
    token = create_access_token({"sub": str(user.id)})

    # set cookie
    # response.set_cookie(key="access_token", value=token, httponly=True)

    # remove password from response
    user.hashed_password = None

    return {"access_token": token, "token_type": "bearer", "data": user}


# @router.post("/admin/logout", tags=["Администраторы"], summary="Выход администратора")
# async def logout_user(response: Response):
#     response.delete_cookie(key="access_token")
#     return {"message": "Logout successful"}


# endregion

# region Auth & Users & Master
@router.post("/user/register", tags=["Auth & Пользователи"], summary="Регистрация пользователя")
async def register_master(user: SUserRegister, request: Request):
    is_user_exist = await UserServices.find_one_or_none(phone=user.phone)

    if is_user_exist:
        raise AlreadyExistsException(f"User with {user.phone} already exists")

    hashed_password = hash_password(user.password)
    user = await UserServices.create(phone=user.phone, hashed_password=hashed_password, role="user")
    return user, {'access_token': create_access_token({"sub": str(user.id)})}


@router.post("/user/social/register", tags=["Auth & Пользователи"], summary="Регистрация пользователя через соц. сети")
async def register_user_social(user: SUserSocialRegister):
    is_user_exist = await UserServices.find_one_or_none(email=user.email)

    if is_user_exist:
        raise UserAlreadyExistsWithThisEmailException

    hashed_password = hash_password(user.password)
    user = await UserServices.create(email=user.email, hashed_password=hashed_password, role="user")
    return user, {'access_token': create_access_token({"sub": str(user.id)})}


@router.post("/master/register", tags=["Мастера"], summary="Регистрация мастера")
async def register_user(user: SMasterRester, request: Request):
    is_user_exist = await UserServices.find_one_or_none(phone=user.phone)

    if is_user_exist:
        raise AlreadyExistsException(f"User with {user.phone} already exists")

    hashed_password = hash_password(user.password)

    user = {
        "phone": user.phone,
        "hashed_password": hashed_password,
        "role": "master",
        "first_name": user.first_name if user.first_name else None,
        "last_name": user.last_name if user.last_name else None,
    }

    return await UserServices.create(**user)


@router.post("/user/login", tags=["Auth & Пользователи"], summary="Авторизация пользователя")
@router.post("/master/login", tags=["Мастера"], summary="Авторизация мастера")
async def login_user(response: Response, user: SUserAuth):
    user = await authenticate_user(phone=user.phone, password=user.password)
    if not user:
        raise UserNotFoundException

    # create access token
    token = create_access_token({"sub": str(user.id)})

    # set cookie
    # response.set_cookie(key="access_token", value=token, httponly=True)

    return {"access_token": token, "token_type": "bearer", "data": user}


@router.post("/user/social/login", tags=["Auth & Пользователи"], summary="Авторизация пользователя через соц. сети")
async def login_user_social(response: Response, user: SUserSocialAuth):
    user = await authenticate_user(email=user.email, password=user.password)
    if not user:
        raise UserNotFoundException

    # create access token
    token = create_access_token({"sub": str(user.id)})

    # set cookie
    # response.set_cookie(key="access_token", value=token, httponly=True)

    return {"access_token": token, "token_type": "bearer", "data": user}


@router.get("/user/me", tags=["Auth & Пользователи"], summary="Получить данные текущего пользователя")
async def get_me(user: Users = Depends(get_current_user)):
    return user


@router.post("/user/{phone}", tags=["Auth & Пользователи"], summary="Получить пользователя по телефону")
async def get_user_by_phone(phone: str):
    user = await UserServices.find_one_or_none(phone=phone)
    print('user ', user)
    if not user:
        raise UserNotFoundException
    return {
        "id": user.id,
        "phone": user.phone,
        "role": user.role
    }


# CRUD
@router.get("/user/all", tags=["Auth & Пользователи"], summary="Получить всех пользователей")
async def get_all_users(
        role: str = None,  # "admin", "user", "master"
        page: int = None,
        limit: int = None,
        search: str = None,
        email: str = None,
):
    return await UserServices.find_all(limit=limit, offset=page, search=search, role=role, email=email, deleted_at=None)


@router.get("/user/{user_id}", tags=["Auth & Пользователи"], summary="Получить пользователя по id")
async def get_user_by_id(user_id: int, user: Users = Depends(get_current_user)):
    return await UserServices.find_one_or_none(id=user_id, deleted_at=None)


@router.patch("/user/{user_id}", tags=["Auth & Пользователи"], summary="Обновить пользователя по id")
async def update_user_by_id(user_id: int, update_user: SUserUpdate):
    # print('id', user_id, update_user.dict())
    if update_user.phone:
        is_user_exist = await UserServices.find_one_or_none(phone=update_user.phone)
        if is_user_exist and is_user_exist.id != user_id:
            raise AlreadyExistsException(f"User with {update_user.phone} already exists")

    if update_user.email:
        is_user_exist = await UserServices.find_one_or_none(email=update_user.email)
        if is_user_exist and is_user_exist.id != user_id:
            raise UserAlreadyExistsWithThisEmailException

    return await UserServices.update(id=user_id, **update_user.dict())


@router.delete("/user/{user_id}", tags=["Auth & Пользователи"], summary="Удалить пользователя по id")
async def delete_user_by_id(user_id: int, user: Users = Depends(get_current_user)):
    return await UserServices.delete(id=user_id)


@router.patch("/user/{user_id}/{device_token}", tags=["Auth & Пользователи"], summary="Обновить divece_token")
async def update_user_by_id(user_id: int, device_token: str):
    return await UserServices.update(id=user_id, device_token=device_token)

# endregion
