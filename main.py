from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import database

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "йоу сасло?"


engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy')
sessions = async_sessionmaker(engine)
