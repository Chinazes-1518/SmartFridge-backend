from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import datetime

import database
import utils

router = APIRouter(prefix='/analytics')



@router.get('/added')
async def get_added_products(
        start_date: datetime,
        end_date: datetime,
        token: Annotated[str, Header()]
) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        result = await session.execute(
            select(database.Analytics)
            .where(database.Analytics.action == "added")
            .where(database.Analytics.date >= start_date)
            .where(database.Analytics.date <= end_date)
        )
        added_products = result.scalars().all()

        added_data = [
            {
                "id": item.id,
                "date": item.date,
                "product_id": item.product_id,
                "details": item.details
            }
            for item in added_products
        ]

        return utils.json_responce({"added_products": added_data})



@router.get('/removed')
async def get_removed_products(
        start_date: datetime,
        end_date: datetime,
        token: Annotated[str, Header()]
) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        result = await session.execute(
            select(database.Analytics)
            .where(database.Analytics.action == "removed")
            .where(database.Analytics.date >= start_date)
            .where(database.Analytics.date <= end_date)
        )
        removed_products = result.scalars().all()

        removed_data = [
            {
                "id": item.id,
                "date": item.date,
                "product_id": item.product_id,
                "details": item.details
            }
            for item in removed_products
        ]

        return utils.json_responce({"removed_products": removed_data})


@router.get('/expired')
async def get_expired_products(
        start_date: datetime,
        end_date: datetime,
        token: Annotated[str, Header()]
) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        result = await session.execute(
            select(database.Analytics)
            .where(database.Analytics.action == "expired")
            .where(database.Analytics.date >= start_date)
            .where(database.Analytics.date <= end_date)
        )
        expired_products = result.scalars().all()

        expired_data = [
            {
                "id": item.id,
                "date": item.date,
                "product_id": item.product_id,
                "details": item.details
            }
            for item in expired_products
        ]
        return utils.json_responce({"expired_products": expired_data})