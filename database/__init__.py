from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database import *

# engine = create_async_engine('postgresql+asyncpg://root:1111@localhost:5432/smartfridge')
engine = create_async_engine('postgresql+asyncpg://neondb_owner:npg_UrhxVXHGm3t9@ep-super-recipe-a873bhyv-pooler.eastus2.azure.neon.tech/neondb')
sessions = async_sessionmaker(engine)

# ./postgres -D 'C:\Users\ученик.313-17\OneDrive\Документы\chupep8\db' -p 5432

