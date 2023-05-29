from pydantic import BaseModel
from typing import Optional

class ServicePrioritySchema(BaseModel):
    id: Optional[int]
    priority: str
    
    class Config:
        orm_mode = True
