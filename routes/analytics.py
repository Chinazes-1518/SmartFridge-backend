from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
import database
import utils
from datetime import datetime

router = APIRouter(prefix='/analytics')


@router.get('/purchases')
async def get_purchase_stats(
        token: Annotated[str, Header()],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
) -> JSONResponse:
    async with database.sessions.begin() as session:
        await utils.verify_token(session, token)

        date_filters = []
        try:
            if start_date:
                start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
                date_filters.append(database.BuyList.date >= start_date_dt)
            if end_date:
                end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
                end_date_dt = end_date_dt.replace(hour=23, minute=59, second=59)
                date_filters.append(database.BuyList.date <= end_date_dt)
            if start_date and end_date and start_date_dt > end_date_dt:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be before or equal to end_date."
                )

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD."
            )
        def create_query(period: str):
            query = select(
                func.date_trunc(period, database.BuyList.date).label("date"),
                database.BuyList.prod_type_id,
                func.sum(database.BuyList.amount).label("total")
            )
            if date_filters:
                query = query.where(*date_filters)
            return query.group_by("date", database.BuyList.prod_type_id).order_by("date")
        daily = await session.execute(create_query('day'))
        monthly = await session.execute(create_query('month'))
        yearly = await session.execute(create_query('year'))
        def format_data(result):
            return [{
                "date": row.date.isoformat(),
                "product_type_id": row.prod_type_id,
                "total": float(row.total) if row.total else 0.0
            } for row in result]

        return JSONResponse({
            "daily": format_data(daily),
            "monthly": format_data(monthly),
            "yearly": format_data(yearly)
        })