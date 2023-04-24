from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import Settings

class BookModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'books'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(256))
    paied = Column(Boolean, default=False)
    created_at = Column(DateTime)
    value = Column(Float(precision=2))
    cost_center_id = Column(Integer, ForeignKey('costcenter.id'))
    cost_center = relationship('CostCenterModel', lazy='joined', back_populates='books', cascade='all')
    service_orders = relationship('ServiceOrderModel', lazy='joined', back_populates='book', uselist=True)
