from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

import database
import utils

router = APIRouter(prefix='/product_categories')


@router.get('/')
async def get_categories() -> str:
    async with database.sessions.begin() as session:
        result = await session.execute(select(database.ProductCategories))
        categories = result.scalars().all()
        return utils.json_responce({"categories": categories})


@router.post('/add')
async def add_category(name: str) -> str:
    async with database.sessions.begin() as session:
        existing = await session.execute(
            select(database.ProductCategories).where(database.ProductCategories.name == name.strip())
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, '{"error": "Категория уже существует"}')
        await session.execute(insert(database.ProductCategories).values(name=name.strip()))
        await session.commit()
        return utils.json_responce({"message": "Категория успешно добавлена"})


@router.delete('/remove/{category_id}')
async def remove_category(category_id: int) -> str:
    async with database.sessions.begin() as session:
        category = await session.execute(
            select(database.ProductCategories).where(database.ProductCategories.id == category_id)
        )
        if not category.scalar_one_or_none():
            raise HTTPException(404, '{"error": "Категория не найдена"}')
        await session.execute(delete(database.ProductCategories).where(database.ProductCategories.id == category_id))
        await session.commit()
        return utils.json_responce({"message": "Категория успешно удалена"})