from sqlalchemy import Column, Integer, ForeignKey
#from sqlalchemy.orm import relationship

from core.configs import Settings

class UserCostcenter(Settings.DB_BASE_MODEL):
    __tablename__ = 'user_costcenter'
    __allow_unmapped__ = True
    
    user_id=Column(Integer, ForeignKey('users.id'), primary_key=True)
    costcenter_id=Column(Integer, ForeignKey('costcenter.id'), primary_key=True)

