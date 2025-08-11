from sqlalchemy import create_engine, text
from datetime import date
from decimal import Decimal

class PostgresDB:
    def __init__(self, host, port, dbname, user, password):
        db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(db_url, echo=False, future=True)

    def call_store_insert(self, ticker, price_date, open_p, high_p, low_p, close_p, volume, adj_close):
        """Gọi stored procedure insert_stock_price"""
        query = text("""
            SELECT stock_raw.insert_stock_price(
                :ticker, :transaction_date, :open_p, :high_p, :low_p,
                :close_p, :adj_close, :volume
            )
        """)
        with self.engine.begin() as conn:  # tự commit khi xong
            conn.execute(query, {
                "ticker": ticker,
                "transaction_date": date.today(),
                "open_p": open_p,
                "high_p": high_p,
                "low_p": low_p,
                "close_p": close_p,
                "adj_close": adj_close,
                "volume": volume
            })
        print(f"✅ Inserted {ticker} - {date.today()}")


db = PostgresDB(
    host="localhost",
    port=5432,
    dbname="stock",
    user="postgres",
    password="tammwg"
)
print("PostgresDB initialized successfully")
# Insert qua stored procedure
db.call_store_insert(
    ticker='HDB',
    price_date=date.today(),
    open_p=Decimal(0),
    high_p=Decimal(0),
    low_p=Decimal(0),
    close_p=Decimal(0),
    volume=Decimal(0),
    adj_close=Decimal(0)
)

# import psycopg2

# conn = psycopg2.connect(
#     dbname="stock",
#     user="postgres",
#     password="tammwg",
#     host="localhost",
#     port="5432"
# )
# cur = conn.cursor()

# cur.execute("""
#     SELECT stock_raw.insert_stock_price(
#         %s::text, %s::date, %s::numeric, %s::numeric, %s::numeric, 
#         %s::numeric, %s::numeric, %s::numeric
#     )
# """, (
#     'ABC', '2025-08-11', 10.5, 11.0, 9.8, 10.9, 10.9, 1000
# ))

# conn.commit()
# cur.close()
# conn.close()

# import psycopg2

# conn = psycopg2.connect(
#     dbname="stock",
#     user="postgres",
#     password="tammwg",
#     host="localhost",
#     port="5432"
# )
# cur = conn.cursor()

# schema_name = 'stock_raw'
# cur.execute("""
#     SELECT routine_name, routine_type
#     FROM information_schema.routines
#     WHERE specific_schema = %s
# """, (schema_name,))

# functions = cur.fetchall()
# print(f"Functions in schema '{schema_name}':")
# for func in functions:
#     print(func)

# cur.close()
# conn.close()