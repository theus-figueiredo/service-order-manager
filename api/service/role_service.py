from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.role_model import RoleModel
from core.dependencies import get_session, validate_access_token


#GET ALL ROLES:
async def get_all_roles(db: AsyncSession = Depends(get_session)):
    
    async with db as database:
        
        query = await database.execute(select(RoleModel))
        all_roles = query.scalars().all()
        
        return all_roles


#GET ROLES BY ID:
async def get_role_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as database:
        
        query = await database.execute(select(RoleModel).filter(RoleModel.id == id))
        role = query.scalars().unique().one_or_none()
        
        return role
