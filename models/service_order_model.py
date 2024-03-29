from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.configs import Settings
from models.book_model import BookModel
from models.service_priority_model import ServicePriorityModel

class ServiceOrderModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_order'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(16))
    description = Column(String(256))
    created_at = Column(DateTime)
    execution_value = Column(Float, nullable=True)
    charged_value = Column(Float, nullable=True)
    status_id = Column(Integer, ForeignKey('service_status.id'))
    status = relationship('ServiceStatusModel', lazy='joined', back_populates='service_orders')
    cost_center_id = Column(Integer, ForeignKey('costcenter.id'))
    cost_center = relationship('CostCenterModel', lazy='joined', back_populates='service_orders')
    category_id = Column(Integer, ForeignKey('service_category.id'))
    category = relationship('ServiceCategoryModel', lazy='joined', back_populates='service_orders')
    comments = relationship('CommentModel', lazy='joined', back_populates='service_order', uselist=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    book = relationship('BookModel', lazy='joined', back_populates='service_orders')
    priority_id = Column(Integer, ForeignKey('service_priority.id'))
    priority = relationship('ServicePriorityModel', lazy='joined', back_populates='service_orders', cascade='all')
