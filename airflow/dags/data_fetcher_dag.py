from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

# Cấu hình DAG
default_args = {
    'owner': 'alpha',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'start_date': datetime(2024, 8, 1),
}

SYMBOLS = ["FPT", "MWG", "HPG", "VIC"]

def call_fetch_api(symbol: str, start: str, end: str):
    url = "http://host.docker.internal:8000/fetch-data/"
    payload = {
        "symbol": symbol,
        "start": start,
        "end": end
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"[SUCCESS] Fetched data for {symbol}: {response.json()}")
    except Exception as e:
        print(f"[ERROR] Lỗi khi fetch dữ liệu cho {symbol}: {e}")

with DAG(
    dag_id="fetch_stock_data_dag",
    default_args=default_args,
    schedule_interval="0 20 * * *",  # Hàng ngày 20h
    catchup=False,
    tags=["stock", "fetch"],
) as dag:

    for symbol in SYMBOLS:
        PythonOperator(
            task_id=f"fetch_{symbol}",
            python_callable=call_fetch_api,
            op_kwargs={
                "symbol": symbol,
                "start": "2025-07-01",
                "end": "{{ ds }}"  # ngày hiện tại theo lịch chạy DAG
            },
        )
