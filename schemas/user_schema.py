from typing import Optional, List
from pydantic import BaseModel

from schemas.role_schema import RoleSchema

class UserBaseSchema(BaseModel):
    id: Optional[int]
    fullname: str
    email: str
    cpf: str
    address: str
    is_admin: Optional[bool] = False
    role_id: Optional[int] = None
    
    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    fullname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    cpf: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool]
    role_id: Optional[int]
    

class UserReturnSchema(UserBaseSchema):
    role: Optional[RoleSchema]


class UserAddCostCenterSchema(UserBaseSchema):
    cost_center_id: int
