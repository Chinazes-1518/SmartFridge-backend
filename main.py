from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager

import database
import routes
import asyncio


# async def create_tables(app: FastAPI) -> None:
#     async with database.engine.begin() as connection:
#         # await connection.run(database.MyBase.metadata.drop_all)
#         await connection.run(database.MyBase.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables in database")
    async with database.engine.begin() as connection:
        # await connection.run(database.MyBase.metadata.drop_all)
        await connection.run_sync(database.MyBase.metadata.create_all)
    yield


# asyncio.run(create_tables())


# app = FastAPI(lifespan=lifespan)
app = FastAPI(lifespan=lifespan)
app.include_router(routes.router)
# database.MyBase.metadata.create_all(bind=database.engine)


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "йоу сасло?"
