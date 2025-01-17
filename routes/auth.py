from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert

import database
import utils

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(login: str, password: str) -> str:
    async with database.sessions.begin() as session:
        request = await session.execute(select(database.Users).where(database.Users.login == login.strip()))
        user = request.scalar_one_or_none()

        print(user)

        if user is None or utils.hash_password(password.strip()) != user.password_hash:
            raise HTTPException(403, "Forbidden")

        token = utils.gen_token()

        print(f'New token for user {user.id} ({user.name}): {token}')

        user2 = user.copy()

        req = await session.execute(select(database.ActiveTokens).where(database.ActiveTokens.user_id == user.id))
        if req.scalar_one_or_none() is None:  # no token for user yet
            print('Adding')
            await session.execute(insert(database.ActiveTokens).values(user_id=user.id, token=token))
            await session.commit()
        else:
            print('Changing')
            req.token = token

        return {
            'token': token,
            'id': user.id,
            'name': user.name
        }
