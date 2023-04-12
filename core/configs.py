from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from os import getenv

load_dotenv()

host = getenv('HOST')
db_port = getenv('DB_PORT')
db_name = getenv('DB_NAME')
db_password = getenv('DB_PASSWORD')
db_username = getenv('DB_USER')

jwt_secret = getenv('JWT_SECRET')

class Settings(BaseSettings):
    
    API_V1_BASE_ENDPOINT: str = '/plazza'
    DB_URL: str = f'postgresql+asyncpg://{db_username}:{db_password}@{host}:{db_port}/{db_name}'
    DB_BASE_MODEL = declarative_base()
    
    JWT_SECRET:str = jwt_secret
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRES_IN_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True


settings = Settings()
