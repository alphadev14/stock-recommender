from fastapi import APIRouter
from typing import List, Dict
from schemas import FetchRequest
from core import data_fetcher, discord_notifier, caculator
from services import stock_service

router = APIRouter(prefix="/api/v1/stocks", tags=["Stocks"])

@router.get("/symbols")
def get_symbols(symbol) -> List[str]:
    """
    Lấy danh sách mã cổ phiếu từ vnstock.
    """
    return data_fetcher.fetch_symbol_vnindex30(symbol)

@router.post("/fetch-data")
def fetch_data(req: FetchRequest):
    """
    Gọi hàm fetch & lưu dữ liệu từ vnstock, tính chỉ báo, lưu vào file.
    """
    file_path = data_fetcher.save_all_data_to_excel(req.symbol, req.start, req.end)
    return {"message": "Success", "file_path": file_path}

@router.post("/fetch-and-save")
def fetch_and_save(req: FetchRequest):
    df = data_fetcher.fetch_quote_data(req.symbol, req.start, req.end)
    data_fetcher.save_price_df_to_db(df, req.symbol)
    discord_notifier.send_discord_notify(req.symbol, req.end)
    return {"message": "Saved to DB"}

@router.post("/indicators")
def stock_indicators(req: FetchRequest):
    df = stock_service.get_stock_prices(req.symbol, req.start, req.end)
    print(f"[DEBUG] Data fetched from DB: {df.head()}")
    # df = stock_service.calculate_indicators(df)
    return df.to_dict(orient="records")

@router.post("/caculate-indicators")
def calculate_indicators(req: FetchRequest):
    df = stock_service.get_stock_prices(req.symbol, req.start, req.end)
    print(f"[DEBUG] Data fetched from DB: {df.head()}")
    df = caculator.calculate_indicators(df)
    return df.to_dict(orient="records")

@router.get("/get-symbol-info")
def get_symbol_info(symbol: str) -> list[dict]:
    return data_fetcher.fetch_symbol_info(symbol)

@router.get("/test")
def test_endpoint():
    """
    Test endpoint to check if the API is working.
    """
    return {"message": "API is working!"}