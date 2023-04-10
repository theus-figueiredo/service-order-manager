from typing import Optional, List
from pydantic import BaseModel

from schemas.role_schema import RoleSchema

class UserBaseSchema(BaseModel):
    id: Optional[int]
    fullname: str
    email: str
    cpf: str
    address: str
    is_admin: bool
    
    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserRoleSchema(UserBaseSchema):
    role: Optional[RoleSchema]


class UserUpdateSchema(UserBaseSchema):
    fullname: Optional[str]
    email: Optional[str]
    cpf: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool]

