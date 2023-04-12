from fastapi import FastAPI

from core.configs import settings
from api.api import api_router

app = FastAPI()

app.include_router(router=api_router, prefix=settings.API_V1_BASE_ENDPOINT)

if __name__ == '__main__':
    import uvicorn
    from dotenv import load_dotenv
    from os import getenv
    
    load_dotenv()
    
    PORT = getenv('PORT')
    HOST = getenv('HOST')
    
    uvicorn.run('main:app', host=HOST, port=int(PORT), reload=True, log_level='info')
