from sqlalchemy import Column, Integer, ForeignKey

from core.configs import Settings

class CostCenterUserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'costcenter_user'
    __allow_unmapped__ = True
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    cost_center_id = Column(Integer, ForeignKey('cost_center.id'), primary_key=True)

