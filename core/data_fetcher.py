from vnstock import Vnstock
import pandas as pd
import os

def fetch_and_save_stock_data(symbol: str, start_date: str, end_date: str, interval: str = "1D") -> str:
    """
    Lấy dữ liệu cổ phiếu và lưu thành file Excel trong thư mục data/
    
    Args:
        symbol (str): mã cổ phiếu (VD: 'MWG')
        start_date (str): ngày bắt đầu (format: YYYY-MM-DD)
        end_date (str): ngày kết thúc (format: YYYY-MM-DD)
        interval (str): khoảng thời gian ('1D', '1W', etc.)

    Returns:
        str: đường dẫn tới file Excel đã lưu
    """
    stock = Vnstock().stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start_date, end=end_date, interval=interval)

    # Đường dẫn tương đối đến thư mục data (cùng cấp với core)
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"stock_raw_{symbol}.xlsx")

    # Lưu file Excel
    df.to_excel(file_path, index=False)

    print(f"[INFO] Đã lưu dữ liệu {symbol} từ {start_date} đến {end_date} vào {file_path}")
    return file_path
