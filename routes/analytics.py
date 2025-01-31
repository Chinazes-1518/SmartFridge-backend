from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import database
import utils

router = APIRouter(prefix='/analytics')


@router.get('/get')
async def get_analytics(start_date: datetime, end_date: datetime, token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        req = await session.execute(select(database.Analytics).where(start_date <= database.Analytics.date).where(database.Analytics.date <= end_date))
        res: list[database.Analytics] = req.scalars().all()

        ret = {
            'total': {
                'added': {},
                'used': {},
                'expired': {}
            },
            'days': []
        }

        for z in res:
            obj = {'date': z.date}
            for val in ('added', 'used', 'expired'):
                obj[val] = sum(z.data[val].values())
                for type_id, amount in z.data[val].items():
                    if type_id in ret['total'][val]:
                        ret['total'][val][type_id] += amount
                    else:
                        ret['total'][val][type_id] = amount
            ret['days'].append(obj)
        
        return utils.json_responce(ret)

# scheduler = AsyncIOScheduler()


# async def check_expired_products():
#     async with database.sessions.begin() as session:
#         today = date.today()
        
#         result = await session.execute(
#             select(database.Products)
#             .where(database.Products.expiration_date < today)
#             .where(database.Products.status != "expired")
#         )
#         expired_products = result.scalars().all()
        
#         for product in expired_products:
#             await session.execute(
#                 update(database.Products)
#                 .where(database.Products.id == product.id)
#                 .values(status="expired")
#             )
            
#             new_analytics = database.Analytics(
#                 action="expired",
#                 product_id=product.id,
#                 date=datetime.now(),
#                 details={
#                     "product_name": product.name,
#                     "expiration_date": str(product.expiration_date)
#                 }
#             )
#             session.add(new_analytics)
        
#         await session.commit()

# scheduler.add_job(
#     check_expired_products,
#     trigger=IntervalTrigger(seconds=30),
#     id="check_expired_products",
#     replace_existing=True
# )


# def start_scheduler():
#     scheduler.start()


# def shutdown_scheduler():
#     scheduler.shutdown()


# @router.get('/added')
# async def get_added_products(
#         start_date: datetime,
#         end_date: datetime,
#         token: Annotated[str, Header()]
# ) -> JSONResponse:
#     async with database.sessions.begin() as session:
#         await utils.verify_token(session, token)

#         result = await session.execute(
#             select(database.Analytics)
#             .where(database.Analytics.action == "added")
#             .where(database.Analytics.date >= start_date)
#             .where(database.Analytics.date <= end_date)
#         )
#         added_products = result.scalars().all()

#         added_data = [
#             {
#                 "id": item.id,
#                 "date": item.date,
#                 "product_id": item.product_id,
#                 "details": item.details
#             }
#             for item in added_products
#         ]

#         return utils.json_responce({"added_products": added_data})


# @router.get('/removed')
# async def get_removed_products(
#         start_date: datetime,
#         end_date: datetime,
#         token: Annotated[str, Header()]
# ) -> JSONResponse:
#     async with database.sessions.begin() as session:
#         await utils.verify_token(session, token)

#         result = await session.execute(
#             select(database.Analytics)
#             .where(database.Analytics.action == "removed")
#             .where(database.Analytics.date >= start_date)
#             .where(database.Analytics.date <= end_date)
#         )
#         removed_products = result.scalars().all()

#         removed_data = [
#             {
#                 "id": item.id,
#                 "date": item.date,
#                 "product_id": item.product_id,
#                 "details": item.details
#             }
#             for item in removed_products
#         ]

#         return utils.json_responce({"removed_products": removed_data})


# @router.get('/expired')
# async def get_expired_products(
#         start_date: datetime,
#         end_date: datetime,
#         token: Annotated[str, Header()]
# ) -> JSONResponse:
#     async with database.sessions.begin() as session:
#         await utils.verify_token(session, token)

#         result = await session.execute(
#             select(database.Analytics)
#             .where(database.Analytics.action == "expired")
#             .where(database.Analytics.date >= start_date)
#             .where(database.Analytics.date <= end_date)
#         )
#         expired_products = result.scalars().all()

#         expired_data = [
#             {
#                 "id": item.id,
#                 "date": item.date,
#                 "product_id": item.product_id,
#                 "details": item.details
#             }
#             for item in expired_products
#         ]
#         return utils.json_responce({"expired_products": expired_data})