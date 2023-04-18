from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from schemas.cost_center_schema import CostCenterBaseSchema
from schemas.service_order_schema import ServiceOrderBaseSchema

class BookBaseSchema(BaseModel):
    
    id: Optional[int]
    description: str
    paied: bool
    created_at: datetime
    value: float
    cost_center_id: int

    class Config:
        orm_mode = True



class BookUpdateSchema(BookBaseSchema):
    description: Optional[str]
    paied: Optional[bool]
    created_at: Optional[datetime]
    value: Optional[float]
    cost_center_id: Optional[int]



class BookReturnSchema(BookBaseSchema):
    id: Optional[int]
    description: Optional[str]
    paied: Optional[bool]
    created_at: Optional[datetime]
    value: Optional[float]
    cost_center: Optional[CostCenterBaseSchema]
    service_orders:Optional[List[ServiceOrderBaseSchema]]

