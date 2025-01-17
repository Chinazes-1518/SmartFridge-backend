from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database import *

engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy')
sessions = async_sessionmaker(engine)
