from vnstock import Vnstock
import pandas as pd
import pandas_ta as ta
import os
from core import db
from models import StockPrice
from datetime import datetime
from sqlalchemy import text
from decimal import Decimal
from typing import List, Dict

# ✅ 1. Lấy dữ liệu giá
def fetch_quote_data(symbol: str, start_date: str, end_date: str, interval: str = "1D") -> pd.DataFrame:
    stock = Vnstock().stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start_date, end=end_date, interval=interval)
    return df

# ✅ 2. Lấy báo cáo tài chính
def fetch_financial_data(symbol: str) -> dict:
    stock = Vnstock().stock(symbol=symbol, source="VCI")
    try:
        return {
            "income_statement": stock.finance.income_statement(),
            "balance_sheet": stock.finance.balance_sheet(),
            "cash_flow": stock.finance.cash_flow()
        }
    except Exception as e:
        print(f"[WARN] Không lấy được báo cáo tài chính của {symbol}: {e}")
        return {}

# ✅ 3. Tính chỉ báo kỹ thuật
def fetch_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if df.empty:
        raise ValueError("DataFrame rỗng — không thể tính chỉ báo kỹ thuật.")
    if df["close"].isnull().any():
        raise ValueError("Cột 'close' có giá trị null — không thể tính chỉ báo kỹ thuật.")

    try:
        print("[DEBUG] Tính RSI...")
        df["rsi"] = ta.rsi(df["close"], length=14)
    except Exception as e:
        print(f"[ERROR] RSI lỗi: {e}")

    try:
        print("[DEBUG] Tính MACD...")
        # Chuyển về float và loại bỏ None
        close_series = df["close"].astype(float).fillna(method="ffill").fillna(method="bfill")

        macd = ta.macd(close_series)
        df["macd"] = macd.get("MACD_12_26_9", pd.Series([None] * len(df)))
        df["signal"] = macd.get("MACDs_12_26_9", pd.Series([None] * len(df)))
    except Exception as e:
        print(f"[ERROR] MACD lỗi: {e}")

    try:
        print("[DEBUG] Tính SMA...")
        df["sma_20"] = ta.sma(df["close"], length=20)
    except Exception as e:
        print(f"[ERROR] SMA lỗi: {e}")

    try:
        print("[DEBUG] Tính EMA...")
        df["ema_20"] = ta.ema(df["close"], length=20)
    except Exception as e:
        print(f"[ERROR] EMA lỗi: {e}")

    print("[DEBUG] Data sau tính toán:")
    print(df.tail())

    return df

# ✅ 4. Lấy chỉ số tham chiếu VNINDEX
def fetch_reference_index(index_symbol: str = "VNINDEX", start_date: str = "2024-01-01", end_date: str = "2025-08-01") -> pd.DataFrame:
    return fetch_quote_data(index_symbol, start_date, end_date)

# ✅ 5. Lấy toàn bộ dữ liệu cổ phiếu
def fetch_all_data(symbol: str, start: str, end: str) -> dict:
    print(f"[INFO] Đang lấy dữ liệu cho mã: {symbol} từ {start} đến {end}")

    df_price = fetch_quote_data(symbol, start, end)

    if df_price.empty:
        print(f"[WARN] Không có dữ liệu giá cho {symbol} trong khoảng {start} đến {end}")
        return {
            "price_with_indicators": pd.DataFrame(),
            "financial_data": {},
            "vnindex": pd.DataFrame()
        }

    df_with_indicators = fetch_technical_indicators(df_price)
    financials = fetch_financial_data(symbol)
    vnindex = fetch_reference_index(start_date=start, end_date=end)

    return {
        "price_with_indicators": df_with_indicators,
        "financial_data": financials,
        "vnindex": vnindex
    }

# ✅ 6. Lưu dữ liệu ra file Excel
def save_all_data_to_excel(symbol: str, start: str, end: str) -> str:
    data = fetch_all_data(symbol, start, end)

    # Đường dẫn lưu vào thư mục /data tại thư mục gốc
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, f"stock_full_{symbol}.xlsx")

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        if not data["price_with_indicators"].empty:
            data["price_with_indicators"].to_excel(writer, sheet_name="Price + Indicators", index=False)
        else:
            print(f"[WARN] Không ghi file giá vì không có dữ liệu cho {symbol}")

        if not data["vnindex"].empty:
            data["vnindex"].to_excel(writer, sheet_name="VNINDEX", index=False)

        if data["financial_data"]:
            for key, df in data["financial_data"].items():
                if not df.empty:
                    sheet_name = key.replace("_", " ").title()
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"[INFO] Dữ liệu đã được lưu tại: {file_path}")
    return file_path

# ✅ 7. Insert DataFrame vào database
def save_price_df_to_db(df, symbol):
    # Kiểm tra kết nối DB và schema trước khi insert
    session = db.SessionLocal()
    try:
        # Kiểm tra kết nối DB
        session.execute(text("SELECT 1"))
        # Kiểm tra schema stock_raw đã tồn tại chưa
        schema_exists = session.execute(
            text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'stock_raw'")
        ).fetchone()
        if not schema_exists:
            session.execute(text("CREATE SCHEMA stock_raw"))
            session.commit()

        for _, row in df.iterrows():
            date_value = row["time"]
            if isinstance(date_value, str):
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
            elif isinstance(date_value, pd.Timestamp):
                date_value = date_value.to_pydatetime().date()
            else:
                date_value = date_value  # datetime.date

            session.execute(
                text("SELECT stock_raw.insert_stock_price(:ticker, :transaction_date, :open_p, :high_p, :low_p, :close_p, :adj_close, :volume)"),
                {
                    "ticker": symbol,
                    "transaction_date": date_value,
                    "open_p": Decimal(row["open"]),
                    "high_p": Decimal(row["high"]),
                    "low_p": Decimal(row["low"]),
                    "close_p": Decimal(row["close"]),
                    "adj_close": Decimal(row["close"]),  # dùng close nếu chưa có adjusted
                    "volume": Decimal(row["volume"])
                }
            )

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Lỗi insert dữ liệu cho {symbol}: {e}")
        raise
    finally:
        session.close()

# ✅ 8. Lấy dữ liệu nhóm cổ phiếu
def fetch_symbol_vnindex30(group_name: str) -> List[str]:
    try:
        stock = Vnstock().stock(symbol="MWG", source="VCI")
        list_symbols = stock.listing.symbols_by_group(group_name)
        return list_symbols
    except Exception as e:
        print(f"[ERROR] Lỗi khi lấy danh sách VNINDEX30: {e}")
        return []

# ✅ 9. Lấy thông tin mã cổ phiếu
def fetch_symbol_info(symbol: str) -> list[dict]:
    try:
        from vnstock import Vnstock
        company = Vnstock().stock(symbol=symbol, source='TCBS').company

        df = company.profile()
        return df.to_dict(orient="records")  # ✅ list of dicts
    except Exception as e:
        print(f"[ERROR] Lỗi khi lấy thông tin cổ phiếu {symbol}: {e}")
        return []