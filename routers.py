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
async def get_last_trading_dates(db: Annotated[AsyncSession, Depends(get_db)], limit_last_dates: int = 5):
    """
    Возвращает даты последних торговых дней.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        limit_last_dates (int): Количество последних торговых дней, которые нужно вернуть.

    Returns:
        list: Список дат последних торговых дней.
    """
    dates = await db.scalars(
        select(TradingResults.date).group_by(TradingResults.date).order_by(TradingResults.date.desc()).limit(
            limit_last_dates))
    return dates.all()


@router.get("/trading_results")
async def get_dynamics(db: Annotated[AsyncSession, Depends(get_db)],
                       search_data: SearchFilterTradingDate = Depends(SearchFilterTradingDate)
                       ):
    """
    Возвращает список торгов по заданному диапазону дат и фильтру.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        search_data (SearchFilterTradingDate): Объект с данными для фильтрации и сортировки.

    Returns:
        dict: Словарь с результатами фильтрации и сортировки.
    """
    tradings = await db.scalars(
        select(TradingResults).where(TradingResults.date.between(search_data.start_date, search_data.end_date),
                                     TradingResults.oil_id == search_data.oil_id if search_data.oil_id else True,
                                     TradingResults.delivery_type_id == search_data.delivery_type_id if search_data.delivery_type_id else True,
                                     TradingResults.delivery_basis_id == search_data.delivery_basis_id if search_data.delivery_basis_id else True,
                                     ))
    return tradings.all()
