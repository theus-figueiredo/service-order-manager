from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from typing import List
from sqlalchemy.orm import relationship

from core.configs import Settings

class UserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    cpf=Column(String(16), nullable=False)
    address=Column(String(256), nullable=False)
    password=Column(String(256), nullable=False)
    is_admin=Column(Boolean, default=False)
    role=relationship('RoleModel', cascade='all', lazy='joined')



    #cost_center_ids=Column(List[Integer], nullable=True, ForeignKey='cost_center.id')
    #cost_center=relationship('CostCenterModel', cascade='all', back_populates='users', uselist=True, lazy='joined')
    