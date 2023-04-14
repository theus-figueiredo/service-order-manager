from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import Settings

class ServiceOrderModel(Settings.DB_BASE_MODEL):
    
    __tablename__ = 'service_order'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(16))
    description = Column(String(256))
    creation_date = Column(Date)
    execution_value = Column(Float(precision=2), nullable=True)
    charged_value = Column(Float(precision=2), nullable=True)
    status_id = Column(Integer, ForeignKey('service_status.id'))
    cost_center_id = Column(Integer, ForeignKey('costcenter.id'))
    status = relationship('ServiceStatusModel', lazy='joined', back_populates='service_orders')
    cost_center = relationship('CostCenterModel', lazy='joined', back_populates='service_orders')
