from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from sqlalchemy.orm import relationship

from core.configs import Settings

class ServiceOrderModel(Settings.DB_BASE_MODEL):
    
    __tablename__ = 'service_orders'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    identifier=Column(String(15), nullable=False)
    description=Column(String(256), nullable=True)
    created_at=Column(Date, nullable=False)
    execution_value=Column(Float(precision=2), nullable=True)
    charging_value=Column(Float(precision=2), nullable=True)

    