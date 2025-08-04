## 📁 Cấu trúc thư mục

Trước khi bắt đầu, đảm bảo bạn có cấu trúc sau trong project:

```
stock-recommender/
├── airflow/                     # Airflow DAGs & config
│   ├── dags/
│   │   └── stock_dag.py         # DAG chính: fetch, calc, notify
│   ├── docker-compose.yml       # Nếu bạn chạy Airflow bằng Docker
│   └── requirements.txt         # Các package cho Airflow
│
├── backend/                     # FastAPI backend
│   ├── main.py                  # API server chính
│   ├── crud.py                  # Truy vấn DB (CRUD)
│   ├── models.py                # ORM models (SQLAlchemy)
│   ├── schemas.py               # Pydantic schemas
│   ├── database.py              # Kết nối Postgres
│   └── requirements.txt         # Dependencies backend
│
├── core/                        # Phần tính toán & xử lý dữ liệu
│   ├── data_fetcher.py          # Lấy dữ liệu cổ phiếu (từ API)
│   ├── calculator.py            # Tính toán P/E, ROE, score...
│   ├── discord_notifier.py      # Gửi tin nhắn Discord
│   └── utils.py                 # Các hàm phụ trợ
│
├── data/                        # Lưu file CSV/JSON tạm thời
│   └── stock_raw_fpt.csv        # Ví dụ dữ liệu 1 mã cổ phiếu
│
├── client/                      # React frontend (Vercel deploy)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/            # fetch() từ backend
│   │   └── App.jsx
│   └── package.json
│
├── .env                         # Biến môi trường dùng chung
├── docker-compose.yml          # Nếu muốn chạy toàn bộ bằng Docker
├── render.yaml                 # Cấu hình deploy backend lên Render
├── README.md

```
