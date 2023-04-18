from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import List

from core.dependencies import get_session, validate_access_token
from schemas.book_schema import BookBaseSchema, BookReturnSchema, BookUpdateSchema
from models.book_model import BookModel
from models.user_model import UserModel

book_router = APIRouter()

#POST
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookReturnSchema)
async def post_book(data: BookBaseSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    if user.is_admin is True:
        new_book = BookModel(
            description = data.description,
            paied = data.paied or False,
            created_at = datetime.now(),
            value = data.value,
            cost_center_id = data.cost_center_id
        )
        
        db.add(new_book)
        await db.commit()
        
        await db.refresh(new_book, ['cost_center', 'service_orders'])
        return new_book



#GET ALL
@book_router.get('/', status_code=status.HTTP_200_OK, response_model=List[BookReturnSchema])
async def get_all_books(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(BookModel))
        all_books = query.scalars().unique().all()
        
        return all_books


#GET BY ID
@book_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=BookReturnSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(BookModel).filter(BookModel.id == id))
        book = query.scalars().unique().one_or_none()
        
        if book:
            return book
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado')



#UPDATE
@book_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=BookReturnSchema)
async def update(id: int, data: BookUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        query = await database.execute(select(BookModel).filter(BookModel.id == id))
        book = query.scalars().unique().one_or_none()
        
        if book:
            if user.is_admin is True:
                
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(book, key, value)
                
                await database.commit()
                return book
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado')


#DDELETE
@book_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        query = await database.execute(select(BookModel).filter(BookModel.id == id))
        book = query.scalars().unique().one_or_none()
        
        if book:
            if user.is_admin is True:
                await database.delete(book)
                await database.commit()
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado')
