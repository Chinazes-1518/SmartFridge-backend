import hashlib
from uuid import uuid4


def hash_password(password: str) -> str:
    return hashlib.sha512((password + 'HJn12B12!').encode("utf-8")).hexdigest()


def gen_token() -> str:
    return str(uuid4())
