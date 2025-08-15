# from pydantic import BaseModel
# from datetime import date
# from typing import Optional

# class StockPriceCreate(BaseModel):
#     ticker: str
#     transactiondate: date
#     priceopen: float
#     pricehigh: float
#     pricelow: float
#     priceclose: float
#     volume: Optional[float] = None

#     class Config:
#         orm_mode = True


# class StockInfoCreate(BaseModel):
#     ticker: str
#     name: Optional[str]
#     exchange: Optional[str]
#     industry: Optional[str]
#     sector: Optional[str]

#     class Config:
#         orm_mode = True
