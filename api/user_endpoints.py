from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel
from models.role_model import RoleModel
from schemas.user_schema import UserBaseSchema, UserCreateSchema, UserRoleSchema, UserUpdateSchema
from core.dependencies import get_session

user_router = APIRouter()
