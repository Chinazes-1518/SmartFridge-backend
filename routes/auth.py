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
            raise HTTPException(403, '{"error": "User not found"}')
        
        if utils.hash_password(password.strip()) != user.password_hash:
            raise HTTPException(403, '{"error": "Password doesnt match"}')

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
