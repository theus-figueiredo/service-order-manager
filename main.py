from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from api.api import api_router

app = FastAPI()

app.include_router(router=api_router, prefix=settings.API_V1_BASE_ENDPOINT)

origins = ['http://localhost:3000']
methods = ['*']
headers = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

if __name__ == '__main__':
    import uvicorn
    from dotenv import load_dotenv
    from os import getenv
    
    load_dotenv()
    
    PORT = getenv('PORT')
    HOST = getenv('HOST')
    
    uvicorn.run('main:app', host=HOST, port=int(PORT), reload=True, log_level='info')
