from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.future import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from pytz import timezone

from core.dependencies import get_session, validate_access_token
from models.service_order_model import ServiceOrderModel
from schemas.service_order_schema import ServiceOrderReturnSchema, ServiceOrderUpdateSchema, ServiceOrderBaseSchema

service_order_router = APIRouter()


#POST
@service_order_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ServiceOrderBaseSchema)
async def post(data: ServiceOrderUpdateSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:

        new_service_order = ServiceOrderModel(
            identifier=data.identifier,
            description=data.description,
            execution_value=None,
            charged_value=None,
            status_id=data.status_id,
            cost_center_id=data.cost_center_id
        )
    
        database.add(new_service_order)
        await database.commit()
    
        return new_service_order


#GET ALL
@service_order_router.get('/', status_code=status.HTTP_200_OK, response_model=List[ServiceOrderReturnSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceOrderModel))
        service_orders: List[ServiceOrderReturnSchema] = query.scalars().unique().all()
        
        return service_orders
    

#GET BY ID
@service_order_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ServiceOrderReturnSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(ServiceOrderModel).filter(ServiceOrderModel.id == id))
        service_order = query.scalars().unique().one_or_none()
        
        if service_order is not None:
            return service_order
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ordem de Serviço não encontrada')


#UPDATE
@service_order_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ServiceOrderReturnSchema)
async def update_os(id: int, new_data: ServiceOrderUpdateSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(ServiceOrderModel).filter(ServiceOrderModel.id == id))
        service_order = query.scalars().unique().one_or_none()
        
        if service_order is not None:
            for key, value in new_data.dict(exclude_unset=True).items():
                setattr(service_order, key, value)
                    
                await database.commit()
                
            return service_order
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ordem de Serviço não encontrada')


#DELETE
@service_order_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(ServiceOrderModel).filter(ServiceOrderModel.id == id))
        service_order = query.scalars().unique().one_or_none()
        
        if service_order is not None:
            await database.delete(service_order)
            await database.commit()
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ordem de Serviço não encontrada')
