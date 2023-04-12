from fastapi import APIRouter

from api.routes.user_routes import user_router
from api.routes.role_routes import role_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix='/users', tags=['users'])
api_router.include_router(router=role_router, prefix='/roles', tags=['roles'])
