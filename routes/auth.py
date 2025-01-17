from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert

import database
import utils

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(username: str, password: str) -> str:
    async with database.sessions.begin() as session:
        request = await session.execute(select(database.Users).where(database.Users.name == username.strip()))
        user = request.scalar_one_or_none()

        # if user is None or utils.hash_password(password.strip()) != user.password:
        #     raise HTTPException(403, "Forbidden")

        token = utils.gen_token()

        # res = await session.execute(insert(database.ActiveTokens).values(user_id=user.id, token=token))
        # session.commit()

        return {}
