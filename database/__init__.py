from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database import *

engine = create_async_engine('postgresql+asyncpg://admin:1111@localhost/smartfridge')
sessions = async_sessionmaker(engine)
