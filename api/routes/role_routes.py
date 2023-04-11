from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_session, validate_access_token
from schemas.role_schema import RoleSchema
from models.role_model import RoleModel
from models.user_model import UserModel


role_router = APIRouter()


#POST
@role_router.post('/', status_code=status.HTTP_201_CREATED, response_model=RoleSchema)
async def post_role(data: RoleSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        try:
            new_role = RoleModel(role=data.role)
            database.add(new_role)
            await database.commit()
            
            return new_role

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Posição já cadastrada')

        
#GET ALL
@role_router.get('/', status_code=status.HTTP_200_OK, response_model=List[RoleSchema])
async def get_all_roles(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(RoleModel))
        roles: List[RoleSchema] = query.scalars().all()
        
        return roles


#GET BY ID
@role_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(RoleModel).filter(RoleModel.id == id))
        role: RoleSchema = query.scalars().unique().one_or_none()
        
        if role:
            return role
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Posição não encontrada')


#UPDATE ROLE
@role_router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def update_role(id: int, data: RoleSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(RoleModel).filter(RoleModel.id == id))
        role_to_update: RoleSchema = query.scalars().unique().one_or_none()
        
        if role_to_update:
            if user.is_admin is True:
                role_to_update.role = data.role
                
                await database.commit()
                return role_to_update
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Posição não enconrada')
