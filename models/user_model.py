from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import Settings

class UserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(256))
    email = Column(String(256), unique=True)
    cpf=Column(String(16), unique=True)
    address=Column(String(256))
    password=Column(String(72))
    is_admin=Column(Boolean, default=False)
    role_id=Column(Integer, ForeignKey('roles.id'), default=None)
    role=relationship('RoleModel', cascade='all', lazy='joined', back_populates='users')
    cost_centers=relationship('CostCenterModel', lazy='joined', back_populates='users', uselist=True, secondary='user_costcenter')
    comments = relationship('CommentModel', lazy='joined', back_populates='user', uselist=True)



class UserCostcenter(Settings.DB_BASE_MODEL):
    __tablename__ = 'user_costcenter'
    __allow_unmapped__ = True
    
    user_id=Column(Integer, ForeignKey('users.id'), primary_key=True)
    costcenter_id=Column(Integer, ForeignKey('costcenter.id'), primary_key=True)

