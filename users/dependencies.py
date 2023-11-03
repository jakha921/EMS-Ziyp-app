from datetime import datetime

import jwt
from fastapi import Request, HTTPException, Depends, status

from config.settings import settings
from users.services import UserServices


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
            raise jwt.ExpiredSignatureError

        # get user_id from payload
        user_id: str = payload.get("sub")
        print('user_id', user_id, type(user_id))
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        # get user from database
        user = await UserServices.find_one_or_none(id=int(user_id))
        print('user', user)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_current_is_admin(current_user: dict = Depends(get_current_user)):
    # if not current_user.role != 'admin':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin")
    return current_user
