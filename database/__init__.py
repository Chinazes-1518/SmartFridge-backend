from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database import *

engine = create_async_engine('postgresql+asyncpg://root:1111@localhost:5432/smartfridge')
sessions = async_sessionmaker(engine)
