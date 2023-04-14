from fastapi import APIRouter

from api.routes.user_routes import user_router
from api.routes.role_routes import role_router
from api.routes.cost_center_routes import costcenter_router
from api.routes.service_category_route import service_category_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix='/users', tags=['users'])
api_router.include_router(router=role_router, prefix='/roles', tags=['roles'])
api_router.include_router(router=costcenter_router, prefix='/cost-center', tags=['Cost center'])
api_router.include_router(router=service_category_router, prefix='/service-category', tags=['service category'])

