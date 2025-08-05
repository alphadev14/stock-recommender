from pydantic import BaseModel
from datetime import date
from typing import Optional

class StockPriceBase(BaseModel):
    ticker: str
    transactiondate: date
    priceopen: Optional[float]
    pricehigh: Optional[float]
    pricelow: Optional[float]
    priceclose: Optional[float]
    volume: Optional[float]

class StockPriceCreate(StockPriceBase):
    pass  # dùng cho insert

class StockPriceOut(StockPriceBase):
    resolution: Optional[str]
    fromsource: Optional[str]

    class Config:
        orm_mode = True  # Cho phép trả object SQLAlchemy
