from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database import *

engine = create_async_engine('postgresql+asyncpg://root:1111@localhost:5432/smartfridge')
sessions = async_sessionmaker(engine)

# ./postgres -D 'C:\Users\ученик.313-17\OneDrive\Документы\chupep8\db' -p 5432
