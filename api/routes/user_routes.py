from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, InternalError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.user_model import UserModel
from schemas.user_schema import UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserReturnSchema
from core.dependencies import get_session, validate_access_token
from core.security import password_hash_generate
from core.autentication import authenticate_user, generate_access_token


user_router = APIRouter()

#POST
@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def post_user(data: UserCreateSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database: 
        try:   
            new_user = UserModel(
                fullname=data.fullname,
                email=data.email,
                password=password_hash_generate(data.password),
                cpf=data.cpf,
                address=data.address,
                is_admin=data.is_admin,
                role_id=(data.role_id or None)
            )
            
            database.add(new_user)
            await database.commit()
            
            return new_user

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email ou CPF já cadastrados')


#GET ALL
@user_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserReturnSchema])
async def get_all(db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(UserModel))
        users: List[UserReturnSchema] = query.scalars().all()
        
        return users


#GET BY ID
@user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserReturnSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)) -> Response:
    
    async with db as database:
        
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user = query.scalars().unique().one_or_none()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
        else:
            return user


#UPDATE USER
@user_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserReturnSchema)
async def update_user(id: int, data: UserUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:

    async with db as database:
        
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user_to_update = query.scalars().unique().one_or_none()
        
        if user_to_update:
            if user_to_update.id == user.id or user.is_admin is True:
                
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(user_to_update, key, value)

                    await database.commit()
                
                return user_to_update
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizado')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')


#DELETE USER
@user_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> None:
    
    async with db as database:
        
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user_to_delete = query.scalars().unique().one_or_none()
        
        if user_to_delete:
            
            if user_to_delete.id == user.id or user.is_admin is True:
                await database.delete(user_to_delete)
                await database.commit()
                
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')


#LOGIN
@user_router.post('/login')
async def login(login_data: UserUpdateSchema, db: AsyncSession = Depends(get_session)) -> Response:
    
    user = await authenticate_user(email=login_data.email, password=login_data.password, db=db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email ou senha incorretos')
    
    return JSONResponse(content={"access_token": generate_access_token(sub=user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)


#UPDATE PASSWORD
@user_router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserReturnSchema)
async def update_password(id: int, data: UserCreateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(validate_access_token)) -> Response:
    
    async with db as database:
        query = await database.execute(select(UserModel).filter(UserModel.id == id))
        user_to_update = query.scalars().unique().one_or_none()
        
        if user_to_update:
            if user_to_update.id == user.id or user.is_admin is True:
                user_to_update.password == password_hash_generate(data.password)
                await database.commit()
                
                return user_to_update
                
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ação não autorizada')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
