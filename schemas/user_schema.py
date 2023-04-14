from typing import Optional, List
from pydantic import BaseModel

from schemas.role_schema import RoleSchema
from schemas.cost_center_schema import CostCenterBaseSchema

class UserBaseSchema(BaseModel):
    id: Optional[int]
    fullname: str
    email: str
    cpf: str
    address: str
    is_admin: Optional[bool]
    role_id: Optional[int]
    
    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str

    class Config:
        orm_mode = True

class UserUpdateSchema(UserBaseSchema):
    fullname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    cpf: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool]
    role_id: Optional[int]
    role: Optional[RoleSchema]
    cost_centers: Optional[List[CostCenterBaseSchema]]
    
    class Config:
        orm_mode = True
    

class UserReturnSchema(UserBaseSchema):
    role: Optional[RoleSchema]
    cost_centers: Optional[List[CostCenterBaseSchema]]
    
    class Config:
        orm_mode = True


class UserUpdateCostCenterSchema(UserBaseSchema):
    fullname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    cpf: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool]
    role_id: Optional[int]
    
    class Config:
        orm_mode = True
