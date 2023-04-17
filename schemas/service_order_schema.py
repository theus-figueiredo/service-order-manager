from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from schemas.service_status_schema import ServiceStatusSchema
from schemas.cost_center_schema import CostCenterBaseSchema

class ServiceOrderBaseSchema(BaseModel):
    id: Optional[int]
    identifier: str
    description: str
    status_id: int
    cost_center_id: int

    class Config:
        orm_mode = True



class ServiceOrderUpdateSchema(ServiceOrderBaseSchema):
    
    identifier: Optional[str]
    description: Optional[str]
    status_id: Optional[int]
    cost_center_id: Optional[int]
    execution_value: Optional[float]
    charged_value: Optional[float]

    class Config:
        orm_mode = True


class ServiceOrderReturnSchema(ServiceOrderBaseSchema):
    identifier: Optional[str]
    description: Optional[str]
    status: Optional[ServiceStatusSchema]
    cost_center: Optional[CostCenterBaseSchema]
    execution_value: Optional[float]
    charged_value: Optional[float]
    
    class Config:
        orm_mode = True
