import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAPI:
    """Тесты API"""

    @pytest.mark.parametrize(
        "limit, res",
        [
            (1, 1),
            (2, 2),
            (3, 3),
            (5, 3),
        ]
    )
    async def test_get_last_trading_dates(
            self, client: AsyncClient,
            limit,
            res
    ):
        """Тест на получение последних дат торгов"""
        params = {
            "limit": limit
        }
        response = await client.get("/last_dates", params=params)

        assert response.status_code == 200
        assert len(response.json()) == res

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, res, status",
        [
            (None, None, None, "2023-01-09", "2025-03-23", 3, 200),
            (None, None, None, "2023-01-09", "2023-03-23", 1, 200),
            (None, None, None, "2023-04-09", "2023-03-23", 1, 422),  # Невалидные данные
            ("A592", None, None, "2023-01-09", "2025-03-23", 1, 200),
            ("A5922", None, None, "2023-01-09", "2025-03-23", 1, 422),  # Невалидные данные
            (None, "A", None, "2023-01-09", "2025-03-23", 2, 200),
            (None, "1", None, "2023-01-09", "2025-03-23", 1, 422),  # Невалидные данные
            (None, None, "AKR", "2023-01-09", "2025-03-23", 1, 200),
            (None, None, "AK1R", "2023-01-09", "2025-03-23", 1, 422),  # Невалидные данные
        ]
    )
    async def test_get_dynamics(
            self, client: AsyncClient,
            oil_id,
            delivery_type_id,
            delivery_basis_id,
            start_date,
            end_date,
            res,
            status
    ):
        """Тест на получение данных по фильтру"""
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        if oil_id is not None:
            params["oil_id"] = oil_id
        if delivery_type_id is not None:
            params["delivery_type_id"] = delivery_type_id
        if delivery_basis_id is not None:
            params["delivery_basis_id"] = delivery_basis_id

        response = await client.get("/trading_dynamic", params=params)
        assert len(response.json()) == res
        assert response.status_code == status

    @pytest.mark.parametrize(
        "limit, oil_id, delivery_type_id, delivery_basis_id, res, status",
        [
            (1, None, None, None, 1, 200),
            (3, None, None, None, 3, 200),
            (5, None, None, None, 3, 200),
            (5, "A592", None, None, 1, 200),
            (5, "A5922", None, None, 1, 422),  # Невалидные данные
            (5, None, "A", None, 2, 200),
            (5, None, "Aa", None, 1, 422),  # Невалидные данные
            (5, None, None, "NVL", 1, 200),
            (5, None, None, "NVAL", 1, 422), # Невалидные данные
        ]
    )
    async def test_get_trading_results(
            self,
            client: AsyncClient,
            limit,
            oil_id,
            delivery_type_id,
            delivery_basis_id,
            res,
            status
    ):
        """Тест на получение списка последних торгов по фильтру"""
        params = {"limit": limit}

        if oil_id is not None:
            params["oil_id"] = oil_id
        if delivery_type_id is not None:
            params["delivery_type_id"] = delivery_type_id
        if delivery_basis_id is not None:
            params["delivery_basis_id"] = delivery_basis_id

        response = await client.get("/last_trading", params=params)
        assert response.status_code == status
        assert len(response.json()) == res

