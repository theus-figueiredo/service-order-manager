from typing import Optional
from pydantic import BaseModel

class RoleSchema(BaseModel):
    id: Optional[int]
    role: str

    class Config:
        orm_mode = True

