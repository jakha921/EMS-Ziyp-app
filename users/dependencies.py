from datetime import datetime

import jwt
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config.settings import settings
from exeptions import NotAuthorizedException, NotValidCredentialsException, UserNotFoundException, TokenExpiredException
from users.services import UserServices


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token),
                           credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    try:
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
