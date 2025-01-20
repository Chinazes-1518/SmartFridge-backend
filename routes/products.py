from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, text
from pydantic import BaseModel
from typing import Annotated

import database
import utils

router = APIRouter(prefix='/products')


@router.get('/all')
async def get_all(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        stmt = text("""
        SELECT products.id AS prod_id, products.production_date, products.expiry_date,
        product_types.name AS type_name, product_types.amount, product_types.units, product_types.id AS type_id,
        product_types.nutritional, product_types.measure_type, product_types.allergens,
        product_categories.name AS cat_name, product_categories.id AS cat_id
        FROM products
        JOIN product_types ON products.type_id = product_types.id
        JOIN product_categories ON product_types.category_id = product_categories.id
        """)

        req = await session.execute(stmt)
        data = req.mappings().all()

        # print(data)

        return utils.json_responce(data)


@router.get('/product')
async def get_product(token: Annotated[str, Header()], id: int) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        stmt = text("""
        SELECT products.id AS prod_id, products.production_date, products.expiry_date,
        product_types.name AS type_name, product_types.amount, product_types.units, product_types.id AS type_id,
        product_types.nutritional, product_types.measure_type, product_types.allergens,
        product_categories.name AS cat_name, product_categories.id AS cat_id
        FROM products
        JOIN product_types ON products.type_id = product_types.id
        JOIN product_categories ON product_types.category_id = product_categories.id
        WHERE products.id = :prod_id
        """)

        req = await session.execute(stmt, {'prod_id': id})
        data = req.mappings().first()

        # print(data)

        if data is None:
            raise HTTPException(404, {'error': 'Продукт с этим id не найден'})

        return utils.json_responce(data)


@router.get('/categories')
async def get_cats(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        req = await session.execute(select(database.ProductCategories))
        data = req.scalars()

        # print(data)

        return utils.json_responce([{'id': x.id, 'name': x.name} for x in data])
