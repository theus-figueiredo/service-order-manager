from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_session, validate_access_token
from models.cost_center_model import CostCenterModel
from schemas.cost_center_schema import CostCenterBaseSchema, CostCenterUpdateSchema
from api.service.cost_center_sevice import get_all_cost_centers, get_cost_center_by_id, update_cost_center

costcenter_router = APIRouter()


#POST
@costcenter_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CostCenterUpdateSchema)
async def post(data: CostCenterBaseSchema, db: AsyncSession = Depends(get_session)):
    
    new_cost_center = CostCenterModel(
        name=data.name,
        address=data.address,
        director=data.director,
        contact=data.contact
    )
    
    db.add(new_cost_center)
    await db.commit()
    
    return new_cost_center


#GET ALL
@costcenter_router.get('/', status_code=status.HTTP_200_OK, response_model=List[CostCenterUpdateSchema])
async def get_all(db: AsyncSession = Depends(get_session)):
    
    return await get_all_cost_centers(db)


#GET BY ID
@costcenter_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CostCenterUpdateSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
        
    cost_center = await get_cost_center_by_id(id, db=db)
    
    if not cost_center:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')
    else:
        return cost_center


#UPDATE
@costcenter_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CostCenterUpdateSchema)
async def update(id: int, data: CostCenterUpdateSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    updated_cost_center = await update_cost_center(id, data, db)

    if updated_cost_center is not None:
        return updated_cost_center
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')


#DELETE
@costcenter_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)) -> None:
    
    cost_center = await get_cost_center_by_id(id, db=db)
    
    if cost_center is not None:
        
        await db.delete(cost_center)
        await db.commit()
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')
