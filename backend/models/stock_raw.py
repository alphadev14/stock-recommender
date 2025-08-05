from sqlalchemy import Column, String, Integer, Date, Numeric, Boolean, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ========== stock_raw.stock_prices ==========
class StockPrice(Base):
    __tablename__ = "stock_prices"
    __table_args__ = {"schema": "stock_raw"}
    __table_args__ = (UniqueConstraint("ticker", "transactiondate", "resolution"), {"schema": "stock_raw"})

    rawid = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    transactiondate = Column(Date, nullable=False)
    priceopen = Column(Numeric(18, 4))
    pricehigh = Column(Numeric(18, 4))
    pricelow = Column(Numeric(18, 4))
    priceclose = Column(Numeric(18, 4))
    priceadjustedclose = Column(Numeric(18, 4))
    volume = Column(Numeric(20, 0))
    resolution = Column(String, default="1D")
    fromsource = Column(String, default="vnstock")
    createddate = Column(TIMESTAMP)
    createduser = Column(String(20), default="administrator")
    updateddate = Column(TIMESTAMP)
    updateduser = Column(String(20))
    deleteddate = Column(TIMESTAMP)
    deleteduser = Column(String(20))
    isdelete = Column(Boolean, default=False)


# ========== stock_raw.stock_info ==========
class StockInfo(Base):
    __tablename__ = "stock_info"
    __table_args__ = {"schema": "stock_raw"}

    ticker = Column(String, primary_key=True)
    name = Column(String)
    exchange = Column(String)
    industry = Column(String)
    sector = Column(String)
    listed_since = Column(Date)
    market_cap = Column(Numeric(20, 0))
    website = Column(Text)
    description = Column(Text)
    createddate = Column(TIMESTAMP)
    createduser = Column(String(20), default="administrator")
    updateddate = Column(TIMESTAMP)
    updateduser = Column(String(20))
    deleteddate = Column(TIMESTAMP)
    deleteduser = Column(String(20))
    isdelete = Column(Boolean, default=False)