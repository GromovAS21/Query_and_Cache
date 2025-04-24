from sqlalchemy import Column, Date, DateTime, Float, Integer, String

from database.db import Base


class TradingResults(Base):
    """Модель для результатов торгов."""

    __tablename__ = "spimex_trading_results"

    id = Column(Integer, primary_key=True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Integer)
    total = Column(Float)
    count = Column(Integer)
    date = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
