import hashlib
from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def json_responce(data: dict) -> JSONResponse:
    return JSONResponse(jsonable_encoder(data))


def hash_password(password: str) -> str:
    return hashlib.sha512((password + 'HJn12B12!').encode("utf-8")).hexdigest()


def gen_token() -> str:
    return str(uuid4())
