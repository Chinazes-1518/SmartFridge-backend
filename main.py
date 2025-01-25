from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import database
import routes
import utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables in database")
    async with database.engine.begin() as connection:
        # await connection.run(database.MyBase.metadata.drop_all)
        await connection.run_sync(database.MyBase.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return utils.json_responce({'data': 'йоу сасло?'})
