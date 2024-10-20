from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import get_auth_data
from app.exceptions import TokenExpireException, NoJwtException, NoUserIdException
from app.entities.users.dao import UserDAO
from app.entities.users.schemas import User
from app.entities.users.auth import get_password_hash
from app.config import settings

def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token
  
async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        raise NoJwtException

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if not expire or expire_time < datetime.now(timezone.utc):
        raise TokenExpireException

    user_id = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return User.from_orm(user)

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role_id == 2:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

async def create_default_admin():
    admin_exists = await UserDAO.find_one_or_none(role_id=2)
    
    if admin_exists:
        return

    admin_data = {
        "username": settings.ADMIN_USERNAME,
        "password": get_password_hash(settings.ADMIN_PASSWORD),
        "role_id": 2,
        "sex": "Мужской"
    }

    await UserDAO.add(**admin_data)