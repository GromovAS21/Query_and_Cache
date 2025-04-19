from typing import AsyncGenerator

from database.db import async_session_maker


async def get_db() -> AsyncGenerator[AsyncGenerator, None]:
    """Создает асинхронную сессию для работы с БД."""
    async with async_session_maker() as session:
        yield session
