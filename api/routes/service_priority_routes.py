from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.dependencies import get_session, validate_access_token
from models.service_priority_model import ServicePriorityModel
from models.user_model import UserModel
from schemas.service_priority_schema import ServicePrioritySchema

service_priority_route = APIRouter()


#POST
@service_priority_route.post('/', status_code=status.HTTP_201_CREATED, response_model=ServicePriorityModel)
async def post_service_priority(data: ServicePrioritySchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        if user.is_admin is True:
            new_priority = ServicePriorityModel(
                priority = data.priority
            )
            
            database.add(new_priority)
            await database.commit()
            
            return new_priority
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")


#GET ALL
@service_priority_route.get('/', status_code=status.HTTP_200_OK, response_model=List[ServicePriorityModel])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query =  await database.execute(select(ServicePriorityModel))
        all_priorities = query.scalars().unique().all()
    
        return all_priorities


#GET BY ID
@service_priority_route.get('/{id}', status_code=status.HTTP_200_OK, response_model=ServicePrioritySchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServicePriorityModel).filter(ServicePriorityModel.id == id))
        service_priority = query.scalars().unique().one_or_none()
        
        if service_priority: return service_priority
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")


#UPDATE
@service_priority_route.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ServicePriorityModel)
async def update_one(id: int, data: ServicePrioritySchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
         
        query = await database.execute(select(ServicePriorityModel).filter(ServicePriorityModel.id == id))
        service_priority = query.scalars().unique().one_or_none()
        
        if service_priority is not None:
            if user.is_admin is True:
                service_priority.priority = data.priority
                
                await database.commit()
                return service_priority
            
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")
    

#DELETE
@service_priority_route.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServicePriorityModel).filter(ServicePriorityModel.id == id))
        service_priority = query.scalars().unique().one_or_none()
        
        if service_priority is not None:
            if user.is_admin is True:
                
                await database.delete(service_priority)
                await database.commit()
            
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")

