from datetime import datetime

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config.settings import settings
from exeptions import NotAuthorizedException, NotValidCredentialsException, UserNotFoundException, TokenExpiredException
from users.services import UserServices

bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        if not credentials:
            raise NotValidCredentialsException

        token = credentials.credentials

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
            raise jwt.ExpiredSignatureError

        # get user_id from payload
        user_id: str = payload.get("sub")
        if not user_id:
            raise NotValidCredentialsException

        # get user from database
        user = await UserServices.find_one_or_none(id=int(user_id))

        if not user:
            raise UserNotFoundException

        return user
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_current_is_admin(current_user: dict = Depends(get_current_user)):
    print('current_user', current_user.role)
    if current_user.role != 'admin':
        raise NotAuthorizedException
    return current_user
