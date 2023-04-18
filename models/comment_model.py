from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.configs import Settings

class CommentModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'comments'
    __allow_unmapped__ = True
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    comment = Column(String(256))
    user_id = Column(Integer, ForeignKey('users.id'))
    posted_at = Column(DateTime)
    user = relationship('UserModel', lazy='joined', back_populates='comments')
    service_order_id = Column(Integer, ForeignKey('service_order.id'))
    service_order = relationship('ServiceOrderModel', lazy='joined', back_populates='comments')
