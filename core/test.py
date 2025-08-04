from data_fetcher import fetch_and_save_stock_data

if __name__ == "__main__":
    # Gọi hàm với tham số mẫu
    symbol = "FPT"
    start = "2025-07-01"
    end = "2025-08-04"
    interval = "1D"

    file_path = fetch_and_save_stock_data(symbol, start, end, interval)
    print(f"Dữ liệu đã được lưu tại: {file_path}")