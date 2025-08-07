from sqlalchemy.orm import Session
from backend.models.stock_raw import StockPrice, StockInfo
from backend.schemas.stock import StockPriceCreate, StockInfoCreate

def insert_stock_price(db: Session, data: StockPriceCreate):
    db_data = StockPrice(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def insert_stock_info(db: Session, data: StockInfoCreate):
    db_data = StockInfo(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data