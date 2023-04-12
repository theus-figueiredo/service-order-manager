from pydantic import BaseModel
from typing import Optional

class CostCenterBaseSchema(BaseModel):
    id: Optional[int]
    name: str
    address: str
    director: str
    contact: str


class CostCenterUpdateSchema(CostCenterBaseSchema):
    name: Optional[str]
    address: Optional[str]
    director: Optional[str]
    contact: Optional[str]

