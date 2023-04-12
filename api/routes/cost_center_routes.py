from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_session, validate_access_token
from schemas.cost_center_schema import CostCenterBaseSchema, CostCentrerUpdateSchema
from models.cost_center_model import CostCenterModel
from models.user_model import UserModel

cost_center_router = APIRouter()


#POST
@cost_center_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CostCenterBaseSchema)
async def post_cost_center(data: CostCenterBaseSchema, db: AsyncSession = Depends(get_session)) -> Response:
    try:
        pass
        async with db as database:
            
            new_cost_center = CostCenterModel(
                name=data.name,
                address=data.address,
                cnpj=data.cnpj,
                monthly_budget=data.monthly_budget
            )
            
            database.add(new_cost_center)
            await database.commit()
            
            return new_cost_center

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='CNPJ já cadastrado')
    

#GET ALL
@cost_center_router.get('/', status_code=status.HTTP_200_OK, response_model=List[CostCenterBaseSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CostCenterModel))
        cost_centers = query.scalars().all()
        
        return cost_centers


#GET BY ID
@cost_center_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CostCenterBaseSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        cost_center = query.scalars().unique().one_or_none()
        
        if cost_center:
            return cost_center
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')


#UPDATE
@cost_center_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CostCenterBaseSchema)
async def update(id: int, new_data: CostCentrerUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        cost_center_to_update = query.scalars().unique().one_or_none()
        
        if cost_center_to_update:
            if user.is_admin is True:
                
                for key, value in new_data.dict(exclude_unset=True).items():
                    setattr(cost_center_to_update, key, value)
                
                await database.commit()
                return cost_center_to_update
            
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')


#DELETE
@cost_center_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> None:
    
    async with db as database:
        query = await database.execute(select(CostCenterModel).filter(CostCenterModel.id == id))
        cost_center_to_delete = query.scalars().unique().one_or_none()
        
        if cost_center_to_delete:
            if user.is_admin is True:
                
                await database.delete(cost_center_to_delete)
                await database.commit()
                
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Centro de custo não encontrado')
