from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models.service_order_model import ServiceOrderModel
from core.configs import Settings

class ServiceStatusModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_status'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    status=Column(String(64))
    service_orders = relationship('ServiceOrderModel', cascade='all', lazy='joined', uselist=True, back_populates='status')
