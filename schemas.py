from datetime import date
from typing import Any

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field, field_validator, model_validator
from starlette import status


class SearchFilterTrading(BaseModel):
    """Схема фильтра для поиска торгов."""

    oil_id: str | None = Field(None, description="Идентификатор топлива", pattern=r"^[A-Z0-9\-]{4}$")
    delivery_type_id: str | None = Field(None, description="Идентификатор типа доставки", pattern=r"^[A-Z]{1}$")
    delivery_basis_id: str | None = Field(None, description="Идентификатор типа базы доставки", pattern=r"^[A-Z]{3}$")


class SearchFilterTradingDate(SearchFilterTrading):
    """Схема фильтра для поиска торгов по диапазону дат."""

    start_date: date = Field(..., description="Дата начала диапазона")
    end_date: date = Field(..., description="Дата конца диапазона")

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, value: Any):
        """Проверяет, что дата начала диапазона не больше текущей даты."""
        if value > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата начала диапазона не может быть больше текущей даты."
            )
        return value

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: Any):
        """Проверяет, что дата конца диапазона не меньше текущей даты."""
        if value > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата конца диапазона не может быть больше текущей даты."
            )
        return value

    @model_validator(mode="after")
    def validate_start_end_date(self):
        """Проверяет, что дата начала диапазона не больше даты конца диапазона."""
        if self.start_date > self.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата начала диапазона не может быть больше даты конца диапазона."
            )
        return self

    @classmethod
    def from_query(cls, query: Query):
        # получаем параметры из URL
        start_date = query.get("start_date")
        end_date = query.get("end_date")
        oil_id = query.get("oil_id")
        delivery_type_id = query.get("delivery_type_id")
        delivery_basis_id = query.get("delivery_basis_id")
        return cls(start_date=start_date, end_date=end_date, oil_id=oil_id, delivery_type_id=delivery_type_id,
                   delivery_basis_id=delivery_basis_id)
