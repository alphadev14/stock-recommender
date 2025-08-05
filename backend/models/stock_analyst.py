from sqlalchemy import Column, String, Integer, Date, Numeric, Boolean, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ========== stock_analyst.financials ==========
class Financial(Base):
    __tablename__ = "financials"
    __table_args__ = (UniqueConstraint("ticker", "period"), {"schema": "stock_analyst"})

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    period = Column(String, nullable=False)
    report_type = Column(String, default="quarter")
    revenue = Column(Numeric(20, 2))
    net_income = Column(Numeric(20, 2))
    eps = Column(Numeric(10, 4))
    roe = Column(Numeric(6, 2))
    roa = Column(Numeric(6, 2))
    pe_ratio = Column(Numeric(10, 4))
    pb_ratio = Column(Numeric(10, 4))
    debt_ratio = Column(Numeric(6, 2))
    createddate = Column(TIMESTAMP)
    createduser = Column(String(20), default="administrator")
    updateddate = Column(TIMESTAMP)
    updateduser = Column(String(20))
    deleteddate = Column(TIMESTAMP)
    deleteduser = Column(String(20))
    isdelete = Column(Boolean, default=False)


# ========== stock_analyst.model_predictions ==========
class ModelPrediction(Base):
    __tablename__ = "model_predictions"
    __table_args__ = (UniqueConstraint("ticker", "date"), {"schema": "stock_analyst"})

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    predicted_price = Column(Numeric(18, 4))
    change_percent = Column(Numeric(6, 2))
    trend = Column(String)
    recommendation = Column(String)
    confidence = Column(Numeric(4, 3))
    model_version = Column(String)
    createddate = Column(TIMESTAMP)
    createduser = Column(String(20), default="administrator")
    updateddate = Column(TIMESTAMP)
    updateduser = Column(String(20))
    deleteddate = Column(TIMESTAMP)
    deleteduser = Column(String(20))
    isdelete = Column(Boolean, default=False)
