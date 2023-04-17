from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import Settings

class ServiceStatusModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_status'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    status=Column(String(32))
    service_orders=relationship('ServiceOrderModel', back_populates='status', lazy='joined', uselist=True)
