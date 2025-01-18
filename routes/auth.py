from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update

import database
import utils

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(login: str, password: str) -> str:
    async with database.sessions.begin() as session:
        request = await session.execute(select(database.Users).where(database.Users.login == login.strip()))
        user = request.scalar_one_or_none()

        if user is None:
            raise HTTPException(403, '{"error": "Пользователя не существует"}')
        
        if utils.hash_password(password.strip()) != user.password_hash:
            raise HTTPException(403, '{"error": "Неправильный пароль"}')

        token = utils.gen_token()

        print(f'New token for user {user.id} ({user.name}): {token}')

        user_id, user_name = user.id, user.name

        user.token = token
        await session.commit()

        return utils.json_responce({
            'token': token,
            'id': user_id,
            'name': user_name
        })


@router.post('/register')
async def register(login: str, password: str, name: str, secret: str) -> str:
    async with database.sessions.begin() as session:
        request = await session.execute(select(database.Users).where(database.Users.login == login.strip()))
        user = request.scalar_one_or_none()

        if secret.strip() != 'saslo228':
            raise HTTPException(403, '{"error": "Нет доступа"}')

        if user is not None:
            raise HTTPException(418, '{"error": "Пользователь уже существует"}')
        
        token = utils.gen_token()

        req = await session.execute(insert(database.Users).values(login=login.strip(), name=name.strip(), password_hash=utils.hash_password(password), token=token))
        await session.commit()

        return utils.json_responce({
            'token': token,
            'id': req.inserted_primary_key[0]
        })
