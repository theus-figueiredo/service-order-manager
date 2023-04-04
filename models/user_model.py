from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from core.configs import Settings

class UserModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password=Column(String(256), nullable=False)
    is_admin=Column(Boolean, default=False)

