from fastapi import status, HTTPException, APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from models.service_status_model import ServiceStatusModel
from schemas.service_status_schema import ServiceStatusSchema
from core.dependencies import get_session


service_status_router = APIRouter()


#POST
@service_status_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ServiceStatusSchema)
async def post(data: ServiceStatusSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    new_status = ServiceStatusModel(status=data.status)
    
    db.add(new_status)
    await db.commit()
    
    return new_status


#GET ALL
@service_status_router.get('/', status_code=status.HTTP_200_OK, response_model=List[ServiceStatusSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceStatusModel))
        all_status = query.scalars().unique().all()
        
        return all_status


#GET BY ID
@service_status_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ServiceStatusSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceStatusModel).filter(ServiceStatusModel.id == id))
        service_status = query.scalars().unique().one_or_none()
        
        if service_status is not None:
            return service_status
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status de serviço não encontrado')


#UPDATE
@service_status_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ServiceStatusSchema)
async def update_status(id: int, data: ServiceStatusSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceStatusModel).filter(ServiceStatusModel.id == id))
        service_status = query.scalars().unique().one_or_none()
        
        if service_status is not None:
            service_status.status = data.status
            
            await database.commit()
            return service_status
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status de serviço não encontrado')


#DELETE
@service_status_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_status(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
       async with db as database:
           
           query = await database.execute(select(ServiceStatusModel).filter(ServiceStatusModel.id == id))
           service_status = query.scalars().unique().one_or_none()
           
           if service_status is not None:
               await database.delete(service_status)
               await database.commit()
            
           else:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status de serviço não encontrado')

