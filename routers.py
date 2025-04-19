from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db
from models import TradingResults
from schemas import SearchFilterTradingDate

router = APIRouter(prefix="", tags=["spimex"])


@router.get("/last_dates")
async def get_last_trading_dates(db: Annotated[AsyncSession, Depends(get_db)], limit: int = 5):
    """
    Возвращает даты последних торговых дней.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        limit (int): Количество последних торговых дней, которые нужно вернуть.

    Returns:
        list: Список дат последних торговых дней.
    """
    dates = await db.scalars(
        select(TradingResults.date).group_by(
            TradingResults.date
        ).order_by(
            TradingResults.date.desc()
        ).limit(
            limit
        ))
    return dates.all()


@router.get("/trading_results")
async def get_dynamics(db: Annotated[AsyncSession, Depends(get_db)],
                       data: SearchFilterTradingDate = Depends(SearchFilterTradingDate)
                       ):
    """
    Возвращает список торгов по заданному диапазону дат и фильтру.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        data (SearchFilterTradingDate): Объект с данными для фильтрации и сортировки.

    Returns:
        dict: Словарь с результатами фильтрации и сортировки.
    """
    tradings = await db.scalars(
        select(TradingResults).where(TradingResults.date.between(
            data.start_date, data.end_date
        ),
            TradingResults.oil_id == data.oil_id if data.oil_id else True,
            TradingResults.delivery_type_id == data.delivery_type_id if data.delivery_type_id else True,
            TradingResults.delivery_basis_id == data.delivery_basis_id if data.delivery_basis_id else True,
        ))
    return tradings.all()
