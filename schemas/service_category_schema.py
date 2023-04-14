from typing import Optional
from pydantic import BaseModel

class ServiceCategorySchema(BaseModel):
    
    id: Optional[int]
    category: str

    class Config:
        orm_mode = True

