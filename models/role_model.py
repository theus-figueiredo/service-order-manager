from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import Settings

class RoleModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'roles'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    role=Column(String(24), unique=True)
