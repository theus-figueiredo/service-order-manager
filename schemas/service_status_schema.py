from typing import Optional
from pydantic import BaseModel

class ServiceStatusSchema(BaseModel):
    
    id: Optional[int]
    status: str
    
    class Config:
        orm_mode = True

