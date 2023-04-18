from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from schemas.service_order_schema import ServiceOrderReturnSchema
from schemas.user_schema import UserReturnSchema

class CommentBaseSchema(BaseModel):
    
    id: Optional[int]
    comment: str
    user_id: int
    posted_at: Optional[datetime]
    service_order_id: int
    
    class Config:
        orm_mode = True


class CommentUpdateSchema(CommentBaseSchema):
    id: Optional[int]
    comment: str
    user_id: Optional[int]
    posted_at: Optional[datetime]
    service_order_id: Optional[int]
    

class CommentReturnSchema(CommentBaseSchema):
    id: int
    comment: str
    posted_at: int
    user: UserReturnSchema
    service_order: ServiceOrderReturnSchema
