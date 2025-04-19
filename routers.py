from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db
from models import TradingResults

router = APIRouter(prefix="", tags=["search"])


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