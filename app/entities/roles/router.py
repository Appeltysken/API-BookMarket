from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.users.dao import UserDAO
from app.entities.users.schemas import User
from app.entities.roles.dao import RoleDAO
from app.entities.users.dependencies import get_current_admin_user

router = APIRouter(prefix='/roles', tags=['Работа с ролями пользователей'])

@router.put("/update/{user_id}", summary="Обновить роль пользователя по ID")
async def update_role_handler(user_id: int, role_id: int, current_user: User = Depends(get_current_admin_user)):
    if current_user.role_id == 2:
        role = await RoleDAO.find_one_or_none_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        user = await UserDAO.find_one_or_none_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = {"role_id": role.id}
        check = await UserDAO.update(user.id, update_data)
        if check:
            return {"message": f"Role with ID '{role_id}' successfully assigned to user {user.username}"}
        else:
            raise HTTPException(status_code=400, detail="Error updating user role")
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update roles")