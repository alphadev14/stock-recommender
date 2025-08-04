from vnstock import Vnstock
import pandas as pd
import pandas_ta as ta
import os

# ✅ 1. fetch_quote_data: Lấy dữ liệu giá
def fetch_quote_data(symbol: str, start_date: str, end_date: str, interval: str = "1D") -> pd.DataFrame:
    stock = Vnstock().stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start_date, end=end_date, interval=interval)
    return df


# ✅ 2. fetch_financial_data: Lấy báo cáo tài chính
def fetch_financial_data(symbol: str) -> dict:
    stock = Vnstock().stock(symbol=symbol, source="VCI")

    try:
        financial_data = {
            "income_statement": stock.finance.income_statement(),
            "balance_sheet": stock.finance.balance_sheet(),
            "cash_flow": stock.finance.cash_flow()
        }
    except Exception as e:
        print(f"[WARN] Không lấy được báo cáo tài chính của {symbol}: {e}")
        financial_data = {}

    return financial_data

# ✅ 3. fetch_technical_indicators: Tính RSI, MACD, EMA...
def fetch_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nhận vào DataFrame giá cổ phiếu, trả về DataFrame kèm chỉ báo kỹ thuật
    """

    df = df.copy()
    df["rsi"] = ta.rsi(df["close"], length=14)
    macd = ta.macd(df["close"])
    df["macd"] = macd["MACD_12_26_9"]
    df["signal"] = macd["MACDs_12_26_9"]

    df["sma_20"] = ta.sma(df["close"], length=20)
    df["ema_20"] = ta.ema(df["close"], length=20)

    return df

# ✅ 4. fetch_reference_index: Lấy chỉ số VNINDEX
def fetch_reference_index(index_symbol: str = "VNINDEX", start_date: str = "2024-01-01", end_date: str = "2025-08-01") -> pd.DataFrame:
    return fetch_quote_data(index_symbol, start_date, end_date)

# ✅ 5. fetch_all_data: Hoàn chỉnh
def fetch_all_data(symbol: str, start: str, end: str) -> dict:
    print(f"[INFO] Đang lấy dữ liệu cho mã: {symbol} từ {start} đến {end}")

    df_price = fetch_quote_data(symbol, start, end)
    df_with_indicators = fetch_technical_indicators(df_price)
    financials = fetch_financial_data(symbol)
    vnindex = fetch_reference_index(start_date=start, end_date=end)

    return {
        "price_with_indicators": df_with_indicators,
        "financial_data": financials,
        "vnindex": vnindex
    }

# ✅ 6. fetch_and_save_stock_data: Lấy và lưu dữ liệu
def save_all_data_to_excel(symbol: str, start: str, end: str, output_folder: str = "../data") -> str:
    data = fetch_all_data(symbol, start, end)

    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"stock_full_{symbol}.xlsx")

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        if data["price_with_indicators"].empty:
          print(f"[WARN] Không có dữ liệu giá cho {symbol} từ {start} đến {end}")
        data["price_with_indicators"].to_excel(writer, sheet_name="Price + Indicators", index=False)
        data["vnindex"].to_excel(writer, sheet_name="VNINDEX", index=False)

        # Ghi từng bảng tài chính vào sheet riêng nếu có
        if data["financial_data"]:
            for key, df in data["financial_data"].items():
                df.to_excel(writer, sheet_name=key.replace("_", " ").title(), index=False)

    print(f"[INFO] Dữ liệu đầy đủ đã lưu vào {file_path}")
    return file_path