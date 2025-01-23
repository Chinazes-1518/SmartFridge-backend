from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import database
import utils
from datetime import datetime

router = APIRouter(prefix='/analytics')


@router.get('/purchases')
async def get_purchase_stats(token: Annotated[str, Header()]) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)
        daily = await session.execute(
            select(
                func.date_trunc('day', database.BuyList.date).label("date"),
                database.BuyList.prod_type_id,
                func.sum(database.BuyList.amount).label("total")
            )
            .group_by("date", database.BuyList.prod_type_id)
            .order_by("date")
        )
        monthly = await session.execute(
            select(
                func.date_trunc('month', database.BuyList.date).label("date"),
                database.BuyList.prod_type_id,
                func.sum(database.BuyList.amount).label("total")
            )
            .group_by("date", database.BuyList.prod_type_id)
            .order_by("date")
        )
        yearly = await session.execute(
            select(
                func.date_trunc('year', database.BuyList.date).label("date"),
                database.BuyList.prod_type_id,
                func.sum(database.BuyList.amount).label("total")
            )
            .group_by("date", database.BuyList.prod_type_id)
            .order_by("date")
        )

        def format_data(result):
            return [{
                "date": row.date.isoformat(),
                "product_type_id": row.prod_type_id,
                "total": row.total
            } for row in result]

        return utils.json_responce({
            "daily": format_data(daily),
            "monthly": format_data(monthly),
            "yearly": format_data(yearly)
        })