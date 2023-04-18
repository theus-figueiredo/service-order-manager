from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from schemas.user_schema import UserBaseSchema

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
    posted_at: datetime
    user_id: Optional[int]
    service_order_id: Optional[int]


class Comment_ServiceOrderSchema(CommentBaseSchema):
    id: Optional[int]
    comment: str
    user_id: int
    user: UserBaseSchema