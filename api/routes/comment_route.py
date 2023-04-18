from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime

from core.dependencies import get_session, validate_access_token
from models.comment_model import CommentModel
from models.user_model import UserModel
from schemas.comment_schema import CommentBaseSchema, CommentReturnSchema, CommentUpdateSchema

comment_router = APIRouter()


#POST
@comment_router.post('/', status_code=status.HTTP_200_OK, response_model=CommentReturnSchema)
async def post_comment(data: CommentUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        new_comment = CommentModel(
            comment = data.comment,
            user_id = user.id,
            posted_at = datetime.now(),
            service_order_id = data.service_order_id
        )
        
        database.add(new_comment)
        await database.commit()
        
        await database.refresh(new_comment, ['user', 'service_order'])
        return new_comment


#GET BY ID
@comment_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CommentReturnSchema)
async def get_comment_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CommentModel).filter(CommentModel.id == id))
        comment = query.scalars().unique().one_or_none()
        
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comentário não encontrado')
        else:
            return comment


#UPDATE COMMENT
@comment_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CommentBaseSchema)
async def update_comment(id: int, data: CommentUpdateSchema,db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(CommentModel).filter(CommentModel.id == id))
        comment = query.scalars().unique().one_or_none()
        
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comentário não encontrado')
        else:
            if user.id == comment.user_id or user.is_admin is True:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(comment, key, value)
                
                await database.commit
                return comment
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')


#DELETE
@comment_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        query = await database.execute(select(CommentModel).filter(CommentModel.id == id))
        comment = query.scalars().unique().one_or_none()
        
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comentário não encontrado')
        else:
            if user.id == comment.user_id or user.is_admin is True:
                await database.delete(comment)
                await database.commit()
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não autorizado')
