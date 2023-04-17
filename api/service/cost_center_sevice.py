from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from models.cost_center_model import CostCenterModel
from schemas.cost_center_schema import CostCenterUpdateSchema


#GET ALL COST-CENTERS:
async def get_all_cost_centers(db: AsyncSession = Depends(get_session)):
    
    async with db as database:
        query = await database.execute(select(CostCenterModel))
        return query.scalars().unique().all()


#GET COST-CENTER BY ID:
async def get_cost_center_by_id(id: int, db: AsyncSession = Depends(get_session)):
    
    async with db as database:
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        return query.scalars().unique().one_or_none()


#UPDATE COST-CENTER:
async def update_cost_center(id: int, data: CostCenterUpdateSchema, db: AsyncSession = Depends(get_session)):
    
    async with db as database:
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        cost_center_to_update = query.scalars().unique().one_or_none()
        
        if cost_center_to_update is None:
            return None
        else:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(cost_center_to_update, key, value)
                
                await database.commit()
            
            return cost_center_to_update
 