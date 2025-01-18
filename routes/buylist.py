from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

import database
import utils

router = APIRouter(prefix='/buylist')


@router.get('/')
async def get_buylist() -> str:
    async with database.sessions.begin() as session:
        result = await session.execute(select(database.BuyList))
        buylist = result.scalars().all()
        return utils.json_responce({"buylist": buylist})
@router.post('/add')
async def add_to_buylist(prod_type_id: int, amount: int) -> str:
    async with database.sessions.begin() as session:
        existing_item = await session.execute(select(database.BuyList).where(database.BuyList.prod_type_id == prod_type_id))
        if existing_item.scalar_one_or_none():
            raise HTTPException(400, '{"error": "Продукт уже есть в списке покупок"}')
        await session.execute(insert(database.BuyList).values(prod_type_id=prod_type_id, amount=amount))
        await session.commit()
        return utils.json_responce({"message": "Продукт успешно добавлен в список покупок"})
@router.delete('/remove/{prod_type_id}')
async def remove_from_buylist(prod_type_id: int) -> str:
    async with database.sessions.begin() as session:
        existing_item = await session.execute(select(database.BuyList).where(database.BuyList.prod_type_id == prod_type_id))
        if not existing_item.scalar_one_or_none():
            raise HTTPException(404, '{"error": "Продукт не найден в списке покупок"}')
        await session.execute(delete(database.BuyList).where(database.BuyList.prod_type_id == prod_type_id))
        await session.commit()
        return utils.json_responce({"message": "Продукт успешно удален из списка покупок"})