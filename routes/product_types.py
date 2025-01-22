from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

import database
import utils

router = APIRouter(prefix='/product_types')


@router.get('/')
async def get_product_types() -> str:
    async with database.sessions.begin() as session:
        result = await session.execute(select(database.ProductTypes))
        product_types = result.scalars().all()
        return utils.json_responce({"product_types": product_types})


@router.post('/add')
async def add_product_type(
    name: str,
    category_id: int,
    amount: float,
    units: str,
    nutritional: int,
    measure_type: str,
    allergens: str = ""
) -> str:
    async with database.sessions.begin() as session:
        category = await session.execute(
            select(database.ProductCategories).where(database.ProductCategories.id == category_id)
        )
        if not category.scalar_one_or_none():
            raise HTTPException(400, '{"error": "Категория не существует"}')
        existing = await session.execute(
            select(database.ProductTypes).where(database.ProductTypes.name == name.strip())
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, '{"error": "Вид продукта уже существует"}')
        await session.execute(
            insert(database.ProductTypes).values(
                name=name.strip(),
                category_id=category_id,
                amount=amount,
                units=units,
                nutritional=nutritional,
                measure_type=measure_type,
                allergens=allergens
            )
        )
        await session.commit()
        return utils.json_responce({"message": "Вид продукта успешно добавлен"})

@router.delete('/remove/{product_type_id}')
async def remove_product_type(product_type_id: int) -> str:
    async with database.sessions.begin() as session:
        product_type = await session.execute(
            select(database.ProductTypes).where(database.ProductTypes.id == product_type_id)
        )
        if not product_type.scalar_one_or_none():
            raise HTTPException(404, '{"error": "Вид продукта не найден"}')
        await session.execute(delete(database.ProductTypes).where(database.ProductTypes.id == product_type_id))
        await session.commit()
        return utils.json_responce({"message": "Вид продукта успешно удален"})



