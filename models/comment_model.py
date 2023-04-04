from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import Settings

class CommentModel(Settings.DB_BASE_MODEL):
    __tablename__ = 'comments'
    __allow_unmapped__ = True
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    comment=Column(String(512), nullable=False)
