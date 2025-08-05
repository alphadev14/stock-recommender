from fastapi import APIRouter
from schemas import FetchRequest
from core import data_fetcher
# from vnstock import listing_companies
from typing import List, Dict

router = APIRouter(prefix="/api/v1/stocks", tags=["Stocks"])


@router.post("/fetch-data")
def fetch_data(req: FetchRequest):
    """
    Gọi hàm fetch & lưu dữ liệu từ vnstock, tính chỉ báo, lưu vào file.
    """
    file_path = data_fetcher.save_all_data_to_excel(req.symbol, req.start, req.end)
    return {"message": "Success", "file_path": file_path}


@router.post("/fetch-data-test")
def fetch_data_test(req: FetchRequest):
    """
    Gọi hàm fetch dữ liệu và lưu CSV để debug.
    """
    df = data_fetcher.fetch_quote_data(req.symbol, req.start, req.end)
    df.to_csv("debug_from_api.csv", index=False)
    return {"status": "done"}


# @router.get("/vnindex30", response_model=List[Dict[str, str]])
# def get_vnindex30():
#     """
#     Trả về danh sách công ty thuộc rổ chỉ số VNINDEX30.
#     """
#     df = listing_companies(
#         exchange='HOSE',
#         type='stock',
#         include_unlisted=False,
#         symbols=None
#     )

#     df30 = df[df['industry'].notnull()].head(30)
#     result = df30[['ticker', 'company_name', 'industry']].to_dict(orient="records")
#     return result
