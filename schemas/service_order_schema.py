from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List

from schemas.service_status_schema import ServiceStatusSchema
from schemas.cost_center_schema import CostCenterBaseSchema
from schemas.service_category_schema import ServiceCategorySchema
from schemas.comment_schema import CommentBaseSchema
from schemas.book_schema import BookBaseSchema

class ServiceOrderBaseSchema(BaseModel):
    id: Optional[int]
    identifier: str
    description: str
    status_id: int
    cost_center_id: int
    category_id: int

    class Config:
        orm_mode = True


class ServiceOrderUpdateSchema(ServiceOrderBaseSchema):
    
    identifier: Optional[str]
    description: Optional[str]
    status_id: Optional[int]
    cost_center_id: Optional[int]
    category_id: Optional[int]
    execution_value: Optional[float]
    charged_value: Optional[float]
    book_id: Optional[int]

    class Config:
        orm_mode = True


class ServiceOrderReturnSchema(ServiceOrderBaseSchema):
    identifier: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    status: Optional[ServiceStatusSchema]
    cost_center: Optional[CostCenterBaseSchema]
    category: Optional[ServiceCategorySchema]
    execution_value: Optional[float]
    charged_value: Optional[float]
    comments: Optional[List[CommentBaseSchema]]
    book: Optional[BookBaseSchema]
    
    class Config:
        orm_mode = True
