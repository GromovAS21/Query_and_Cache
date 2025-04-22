from datetime import date

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator


class SearchFilterTrading(BaseModel):
    """Схема фильтра для поиска торгов."""

    oil_id: str | None = Field(
        None, description="Идентификатор топлива", pattern=r"^[A-Z0-9\-]{4}$"
    )
    delivery_type_id: str | None = Field(
        None, description="Идентификатор типа доставки", pattern=r"^[A-Z]{1}$"
    )
    delivery_basis_id: str | None = Field(
        None, description="Идентификатор типа базы доставки", pattern=r"^[A-Z]{3}$"
    )


class SearchFilterTradingDate(SearchFilterTrading):
    """Схема фильтра для поиска торгов по диапазону дат."""

    start_date: date = Field(..., description="Дата начала диапазона", le=date.today())
    end_date: date = Field(..., description="Дата конца диапазона", le=date.today())

    @model_validator(mode="after")
    def validate_start_end_date(self):
        """Проверяет, что дата начала диапазона не больше даты конца диапазона."""
        if self.start_date > self.end_date:
            raise RequestValidationError([{"loc": ["start_date", "end_date"], "msg": "Дата начала диапазона не может быть больше даты конца диапазона.", "type": "value_error"}])
        return self