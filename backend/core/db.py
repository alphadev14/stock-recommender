# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Lấy URL của database từ biến môi trường
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "stock")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "tammwg")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Kiểm tra nếu thiếu URL thì raise lỗi rõ ràng
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Tạo engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True để debug SQL nếu cần

# Tạo session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để kế thừa trong các model
Base = declarative_base()
