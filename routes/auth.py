from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update
from pydantic import BaseModel, constr
from typing import Optional

import database
import utils

router = APIRouter(prefix='/auth')



class LoginRequest(BaseModel):
    login: str
    password: str


class RegisterRequest(BaseModel):
    name: constr(min_length=1, max_length=100)
    login: constr(min_length=5, max_length=100)
    password: constr(min_length=5, max_length=100)
    secret: str


class VerifyRequest(BaseModel):
    token: str


@router.post('/login', response_class=JSONResponse)
async def login(data: LoginRequest):
    async with database.sessions.begin() as session:
        result = await session.execute(
            select(database.Users)
            .where(database.Users.login == data.login.strip())
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "Пользователь не найден"}
            )


        if utils.hash_password(data.password.strip()) != user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "Неверный пароль"}
            )

        new_token = utils.gen_token()
        await session.execute(
            update(database.Users)
            .where(database.Users.id == user.id)
            .values(token=new_token)
        )
        await session.commit()

        return utils.json_responce({
            "token": new_token,
            "id": user.id,
            "name": user.name
        })


@router.post('/register', response_class=JSONResponse)
async def register(data: RegisterRequest):
    async with database.sessions.begin() as session:
        if data.secret.strip() != 'saslo228':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "Неверный секретный код"}
            )

        existing_user = await session.execute(
            select(database.Users)
            .where(database.Users.login == data.login.strip())
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Логин уже занят"}
            )
        token = utils.gen_token()
        result = await session.execute(
            insert(database.Users)
            .values(
                login=data.login.strip(),
                name=data.name.strip(),
                password_hash=utils.hash_password(data.password),
                token=token
            )
            .returning(database.Users.id)
        )
        await session.commit()

        return utils.json_responce({
            "token": token,
            "id": result.scalar_one()
        })


@router.post('/verify', response_class=JSONResponse)
async def verify(data: VerifyRequest):
    async with database.sessions.begin() as session:
        result = await session.execute(
            select(database.Users)
            .where(database.Users.token == data.token.strip())
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "Неверный токен"}
            )

        return utils.json_responce({
            "id": user.id,
            "login": user.login,
            "name": user.name
        })