from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

import database
import utils

router = APIRouter(prefix='/buylist')


@router.get('/get')
async def get_buylist() -> str:
    async with database.sessions.begin() as session:
        result = await session.execute(select(database.BuyList))
        buylist = result.scalars().all()
        return utils.json_responce({"buylist": buylist})


class BuylistAdd(BaseModel):
    prod_type_id: int
    amount: int
    

@router.post('/add')
async def add_to_buylist(data: BuylistAdd) -> str:
    async with database.sessions.begin() as session:
        existing_item = await session.execute(select(database.BuyList).where(database.BuyList.prod_type_id == data.prod_type_id))
        if existing_item.scalar_one_or_none():
            raise HTTPException(400, '{"error": "Продукт уже есть в списке покупок"}')
        await session.execute(insert(database.BuyList).values(prod_type_id=data.prod_type_id, amount=data.amount))
        await session.commit()
        return utils.json_responce({"message": "Продукт успешно добавлен в список покупок"})


@router.delete('/remove/{buylist_id}')
async def remove_from_buylist(buylist_id: int) -> str:
    async with database.sessions.begin() as session:
        existing_item = await session.execute(select(database.BuyList).where(database.BuyList.id == buylist_id))
        if not existing_item.scalar_one_or_none():
            raise HTTPException(404, '{"error": "Продукт не найден в списке покупок"}')
        await session.execute(delete(database.BuyList).where(database.BuyList.id == buylist_id))
        await session.commit()
        return utils.json_responce({"message": "Продукт успешно удален из списка покупок"})
