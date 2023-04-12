from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_session, validate_access_token
from models.cost_center_model import CostCenterModel
from schemas.cost_center_schema import CostCenterBaseSchema, CostCenterUpdateSchema

costcenter_router = APIRouter()


#POST
@costcenter_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CostCenterBaseSchema)
async def post(data: CostCenterBaseSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
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
@costcenter_router.get('/', status_code=status.HTTP_200_OK, response_model=List[CostCenterBaseSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CostCenterModel))
        cost_centers = query.scalars().all()
        
        return cost_centers


#GET BY ID
@costcenter_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CostCenterBaseSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        cost_center = query.scalars().unique().one_or_none()
        
        if not cost_center:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')
        else:
            return cost_center
