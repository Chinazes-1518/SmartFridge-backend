from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import database
import utils

router = APIRouter(prefix='/product_types')


@router.get('/all')
async def get_types(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        req = await session.execute(select(database.ProductTypes))
        data = list(map(lambda x: (x.__dict__, x.__dict__.pop('_sa_instance_state'))[0],
                        req.scalars()))  # hack to remove a sqlalchemy key inside lambda

        # print(data)

        return utils.json_responce(data)


@router.post('/add')
async def add_product_type(
        token: Annotated[str, Header()],
        name: str,
        category_id: int,
        amount: float,
        units: str,
        nutritional: int,
        measure_type: str,
        allergens: str = ""
) -> str:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        category = await session.execute(
            select(database.ProductCategories).where(database.ProductCategories.id == category_id)
        )
        if not category.scalar_one_or_none():
            raise HTTPException(400, {"error": "Категория не существует"})
        existing = await session.execute(
            select(database.ProductTypes).where(database.ProductTypes.name == name.strip())
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, {"error": "Вид продукта уже существует"})
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
async def remove_product_type(token: Annotated[str, Header()], product_type_id: int) -> str:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        product_type = await session.execute(
            select(database.ProductTypes).where(database.ProductTypes.id == product_type_id)
        )
        if not product_type.scalar_one_or_none():
            raise HTTPException(404, {"error": "Вид продукта не найден"})
        await session.execute(delete(database.ProductTypes).where(database.ProductTypes.id == product_type_id))
        await session.commit()
        return utils.json_responce({"message": "Вид продукта успешно удален"})
