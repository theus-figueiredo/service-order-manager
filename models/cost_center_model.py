from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from core.configs import Settings

class CostCenterModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'costcenter'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(256))
    address=Column(String(256))
    director=Column(String(52))
    contact=Column(String(64))
    users=relationship('UserModel', back_populates='cost_centers', cascade='all', secondary='user_costcenter', uselist=True)
    service_orders=relationship('ServiceOrderModel', back_populates='cost_center', cascade='all', lazy='joined', uselist=True)
    books = relationship('BookModel', lazy='joined', back_populates='cost_center', uselist=True, cascade='all')
