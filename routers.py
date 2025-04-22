from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import trading_key_builder, last_dates_key_builder
from constaints import default_limit, get_cache_expiration
from database.db_depends import get_db
from models import TradingResults
from schemas import SearchFilterTradingDate, SearchFilterTrading

router = APIRouter(prefix="", tags=["spimex"])


@router.get("/last_dates")
@cache(expire=get_cache_expiration(), key_builder=last_dates_key_builder)
async def get_last_trading_dates(
        db: Annotated[AsyncSession, Depends(get_db)], limit: int = default_limit
):
    """
    Возвращает даты последних торговых дней.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        limit (int): Количество последних торговых дней, которые нужно вернуть.

    Returns:
        list: Список дат последних торговых дней.
    """
    dates = await db.scalars(
        select(TradingResults.date)
        .group_by(TradingResults.date)
        .order_by(TradingResults.date.desc())
        .limit(limit)
    )
    return dates.all()


@router.get("/trading_dynamic")
@cache(expire=get_cache_expiration(), key_builder=trading_key_builder)
async def get_dynamics(
        db: Annotated[AsyncSession, Depends(get_db)],
        data: SearchFilterTradingDate = Depends(SearchFilterTradingDate),
):
    """
    Возвращает список торгов по заданному диапазону дат и фильтру.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        data (SearchFilterTradingDate): Объект с данными для фильтрации и сортировки.

    Returns:
        dict: Словарь с результатами фильтрации.
    """
    tradings = await db.scalars(
        select(TradingResults).where(
            TradingResults.date.between(data.start_date, data.end_date),
            TradingResults.oil_id == data.oil_id
            if data.oil_id else True,
            (
                TradingResults.delivery_type_id == data.delivery_type_id
                if data.delivery_type_id else True
            ),
            (
                TradingResults.delivery_basis_id == data.delivery_basis_id
                if data.delivery_basis_id else True
            ),
        )
    )
    return tradings.all()


@router.get("/last_trading")
@cache(expire=get_cache_expiration(), key_builder=trading_key_builder)
async def get_trading_results(
        db: Annotated[AsyncSession, Depends(get_db)],
        data: SearchFilterTrading = Depends(SearchFilterTrading),
        limit: int = default_limit,
):
    """
    Возвращает список результатов торгов поcледние и фильтру.

    Args:
        db (AsyncSession): Сессия для работы с БД.
        data (SearchFilterTrading): Объект с данными для фильтрации и сортировки.
        limit (int): Количество последних торговых дней, которые нужно вернуть.

    Returns:
        dict: Словарь с результатами фильтрации.
    """
    tradings = await db.scalars(
        select(TradingResults)
        .where(
            TradingResults.oil_id == data.oil_id
                        if data.oil_id else True,
            (
                TradingResults.delivery_type_id == data.delivery_type_id
                if data.delivery_type_id else True
            ),
            (
                TradingResults.delivery_basis_id == data.delivery_basis_id
                if data.delivery_basis_id else True
            ),
        )
        .order_by(TradingResults.date.desc())
        .limit(limit)
    )
    return tradings.all()
