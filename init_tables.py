from core.configs import settings
from database.database_session import engine

async def create_tables() -> None:
    import models.__all_models
    print('Criando tabelas...')
    
    async with engine.begin() as connection:
        await connection.run_sync(settings.DB_BASE_MODEL.metadata.drop_all)
        await connection.run_sync(settings.DB_BASE_MODEL.metadata.create_all)
        
        print('Tabelas criadas')


if __name__ == '__main__':
    import asyncio
    
    asyncio.run(create_tables())
