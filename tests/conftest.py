import asyncio
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import config
from database.db import Base, engine
from main import app
from models import TradingResults


@pytest.fixture(scope="session")
def event_loop():
    """Создает новый цикл событий для тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_cache():
    """Инициализирует in-memory кэш для тестов (фактически отключает кэширование)"""
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache-test")
    yield
    await FastAPICache.clear()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Создает базу данных для тестов."""
    assert config.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        dates = [
            TradingResults(
                exchange_product_id="A592AKR060F",
                exchange_product_name="Бензин (АИ-92-К5) по ГОСТ, ст. Аксарайская II (ст. отправления)",
                oil_id="A592",
                delivery_basis_id="AKR",
                delivery_basis_name="ст. Аксарайская II",
                delivery_type_id="F",
                volume=1440,
                total=52917120,
                count=19,
                date=datetime.strptime("2023-01-09", "%Y-%m-%d"),
            ),
            TradingResults(
                exchange_product_id="A925KIT025A",
                exchange_product_name="Бензин Регуляр-92 (АИ-92-К5), КИНЕФ (самовывоз автотранспортом)",
                oil_id="A925",
                delivery_basis_id="KIT",
                delivery_basis_name="КИНЕФ",
                delivery_type_id="A",
                volume=650,
                total=25165000,
                count=11,
                date=datetime.strptime("2024-10-01", "%Y-%m-%d"),
            ),
            TradingResults(
                exchange_product_id="DSC5NVL005A",
                exchange_product_name="ДТ ЕВРО сорт C (ДТ-Л-К5) минус 5, ЛПДС Невская (самовывоз автотранспортом)",
                oil_id="DSC5",
                delivery_basis_id="NVL",
                delivery_basis_name="ЛПДС Невская",
                delivery_type_id="A",
                volume=115,
                total=5819000,
                count=4,
                date=datetime.strptime("2025-03-23", "%Y-%m-%d"),
            ),
        ]
        session.add_all(dates)
        await session.commit()


@pytest_asyncio.fixture
async def client():
    """Создает асинхронный клиент для тестов."""
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
