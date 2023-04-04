from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import Settings

class ServiceStatusModel(Settings.DB_BASE_MODEL):
    __tabelname__ = 'service_status'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    status=Column(String(24))
