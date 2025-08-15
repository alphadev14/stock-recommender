from sqlalchemy.orm import Session
import pandas as pd
import pandas_ta as ta
from core import db

# 4. Lấy dữ liệu giá cổ phiếu từ database
def get_stock_prices(symbol: str, start_date, end_date):
    with db.SessionLocal() as session:
        sql = """
            SELECT * FROM stock_raw.stock_prices_get(:symbol, :start_date, :end_date)
        """
        result = session.execute(sql, {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })
        return pd.DataFrame(result.mappings())
