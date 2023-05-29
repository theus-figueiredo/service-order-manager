from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from core.configs import Settings

class ServicePriorityModel(Settings.DB_BASE_MODEL):
    __tablename__ = "service_priority"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String())
    service_orders = relationship('ServiceOrderModel', lazy='joined', back_populates='priority', uselist=True, cascade='all')