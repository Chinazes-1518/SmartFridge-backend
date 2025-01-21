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

        print(data)

        cats = list(set([x['cat_name'] for x in data]))
        print(cats)

        # types = {
        #     cat:{
        #         'items': list(set([x['type_name'] for x in data if x['cat_name'] == cat]))
        #     } for cat in cats
        # }
        # print(types)

        res = {}
        for cat in set([x['cat_name'] for x in data]):
            types = [x for x in data if x['cat_name'] == cat]
            # print(cat, types)
            res[cat] = {}
            for t in types:
                t = dict(t)
                # print(t)
                # del t['prod_id']
                # del t['type_name']
                # del t['type_id']
                # del t['cat_id']
                # del t['cat_name']
                # t.pop('prod_id')
                # print(t)
                t2 = {key: t[key] for key in
                      ['type_id', 'amount', 'units', 'nutritional', 'measure_type', 'allergens']}
                # print(t2)
                t2['items'] = []
                for z in data:
                    if z['cat_name'] == cat and z['type_id'] == t['type_id']:
                        # print('!!!', z)
                        t3 = {key: t[key] for key in ['prod_id', 'production_date', 'expiry_date']}
                        t2['items'].append(t3)
                res[cat][t['type_name']] = t2
        # print()
        # print()
        # print()
        # print()
        # print()
        # print()

        # print(res)

        return utils.json_responce(res)


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


@router.get('/types')
async def get_types(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        req = await session.execute(select(database.ProductTypes))
        data = list(map(lambda x: (x.__dict__, x.__dict__.pop('_sa_instance_state'))[0],
                        req.scalars()))  # hack to remove a sqlalchemy key inside lambda

        # print(data)

        return utils.json_responce(data)
