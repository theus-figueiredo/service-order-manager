from sqlalchemy import Column, Integer, String

from core.configs import Settings

class ServiceCategoryModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_category'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(64))
