from sqlalchemy import Column, Integer, String

from core.configs import Settings

class ServiceCategory(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_category'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cetegory = Column(String(64))
