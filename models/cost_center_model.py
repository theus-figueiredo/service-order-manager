from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from core.configs import Settings

class CostCenterModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'cost_center'
    __allow_unmapped__ =  True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(256), nullable=False)
    address=Column(String(256), nullable=False)
    cnpj=Column(String(16), nullable=False, unique=True)
    monthly_budget=Column(Float(precision=2))
    users = relationship('UserModel', back_populates='cost_center', secondary='costcenter_user', uselist=True)
