from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config.settings import settings
from users.services import UserServices

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(password: str, phone: str = None, email: EmailStr = None):
    if phone:
        user = await UserServices.find_one_or_none(phone=phone, deleted_at=None)
    elif email:
        user = await UserServices.find_one_or_none(email=email, deleted_at=None)

    print('user', user.__dict__)

    if user and verify_password(password, user.hashed_password):
        return user
