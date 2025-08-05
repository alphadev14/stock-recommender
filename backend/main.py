import sys
import os

# Thêm đường dẫn tới thư mục gốc để import core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from schemas import FetchRequest  # Đảm bảo schemas.py nằm trong cùng thư mục với main.py
from core import data_fetcher  # Đảm bảo core/ nằm cùng cấp với backend/
import uvicorn

app = FastAPI(title="Stock Data API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Stock Data API!"}

@app.post("/fetch-data/")
def fetch_data(req: FetchRequest):
    try:
        print(f"[INFO] Fetching data for {req.symbol} from {req.start} to {req.end}")
        file_path = data_fetcher.save_all_data_to_excel(req.symbol, req.start, req.end)
        print(f"[INFO] Dữ liệu đã được lưu vào {file_path}")
        return {"message": "Success", "file_path": file_path}
    except Exception as e:
        return {"message": "Failed", "error": str(e)}

@app.post("/fetch-data-test/")
def fetch_data_endpoint(req: FetchRequest):
    df = data_fetcher.fetch_quote_data(req.symbol, req.start, req.end)
    df.to_csv("debug_from_api.csv", index=False)
    return {"status": "done"}

# Chạy trực tiếp bằng `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
