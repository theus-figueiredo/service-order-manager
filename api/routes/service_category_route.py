from fastapi import APIRouter, Response, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from models.service_category_model import ServiceCategoryModel
from schemas.service_category_schema import ServiceCategorySchema
from core.dependencies import get_session

service_category_router = APIRouter()

#POST
@service_category_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ServiceCategorySchema)
async def post(data: ServiceCategorySchema, db: AsyncSession = Depends(get_session)):
        
    new_category = ServiceCategoryModel(category=data.category)
    db.add(new_category)
        
    await db.commit()
        
    return new_category

#GET ALL
@service_category_router.get('/', status_code=status.HTTP_200_OK, response_model=List[ServiceCategorySchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceCategoryModel))
        categories = query.scalars().unique().all()
        
        return categories


#GET BY ID
@service_category_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ServiceCategorySchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(ServiceCategoryModel).filter(ServiceCategoryModel.id == id))
        categories = query.scalars().unique().one_or_none()
        
        if categories is not None:
            return categories
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada')
    

#UPDATE
@service_category_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ServiceCategorySchema)
async def update(id: int, new_data: ServiceCategorySchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(ServiceCategoryModel).filter(ServiceCategoryModel.id == id))
        category = query.scalars().unique().one_or_none()
        
        if category is not None:
            category.category = new_data.category
            await database.commit()
            
            return category
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada')


#DELETE
@service_category_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(ServiceCategoryModel).filter(ServiceCategoryModel.id == id))
        category = query.scalars().unique().one_or_none()
        
        if category is not None:
            await database.delete(category)
            await database.commit()
            
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada')
