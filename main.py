from typing import Union
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# engine = create_engine('sqlite:///sqlite3.db')
# engine.connect()

engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy')
sessions = async_sessionmaker(engine)