from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from core.configs import Settings

class ServiceStatusModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'service_status'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    status=Column(String(64))
