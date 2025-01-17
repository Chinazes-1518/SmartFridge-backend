from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import database
import routes

app = FastAPI()
app.include_router(routes.router)


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "йоу сасло?"


