from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, text
from pydantic import BaseModel
from typing import Annotated

import database
import utils

router = APIRouter(prefix='/products')


@router.get('/get_all')
async def get_all(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        stmt = text("""
        SELECT products.id AS prod_id, products.production_date, products.expiry_date,
        product_types.name AS type_name, product_types.amount, product_types.units,
        product_types.nutritional, product_types.measure_type, product_types.allergens,
        product_categories.name AS cat_name
        JOIN product_types ON products.type_id = product_types.id
        JOIN product_categories ON product_types.category_id = product_categories.id
        WHERE products.id = 3
        """).columns(
            database.Products.id, database.Products.production_date, database.Products.expiry_date,
            database.ProductTypes.name, database.ProductTypes.amount, database.ProductTypes.units,
            database.ProductTypes.nutritional, database.ProductTypes.measure_type, database.ProductTypes.allergens,
            database.ProductCategories.name
        )

        data = await session.execute(select(database.Products))

        print(data.fetchone())
        # for pr in data.scalars().fetchall():
        #     print(pr)