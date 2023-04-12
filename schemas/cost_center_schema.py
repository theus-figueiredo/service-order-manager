from typing import Optional
from pydantic import BaseModel


class CostCenterBaseSchema(BaseModel):
    id: Optional[int]
    name: str
    address: str
    cnpj: str
    monthly_budget: float


class CostCentrerUpdateSchema(CostCenterBaseSchema):
    name: Optional[str]
    cnpj: Optional[str]
    address: Optional[str]
    monthly_budget: Optional[float]

