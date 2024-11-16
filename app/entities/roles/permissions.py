from fastapi import Depends, HTTPException, status
from functools import wraps
from app.entities.users.dependencies import get_current_user
from app.entities.users.schemas import User as SUser

def permissions(access_type: str = "authorized"):
    
    def decorator(route_function):
        @wraps(route_function)
        
        async def wrapper(id: int = None, current_user: SUser = Depends(get_current_user), *args, **kwargs):
            
            if access_type == "authorized":
                if current_user:
                    return await route_function(current_user=current_user, *args, **kwargs)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Требуется авторизация.")
            
            if access_type == "self_or_admin":
                if current_user.id == id or current_user.role_id == 2:
                    return await route_function(id=id, current_user=current_user, *args, **kwargs)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

            if access_type == "admin":
                if current_user.role_id == 2:
                    return await route_function(current_user=current_user, *args, **kwargs)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неверный тип доступа")

        return wrapper
    
    return decorator