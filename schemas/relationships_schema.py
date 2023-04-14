from typing import Optional
from pydantic import BaseModel

class UserCostcenterBaseSchema(BaseModel):
    
    user_id: Optional[int]
    costcenter_id: Optional[int]
    
    class Condig:
        orm_mode = True

