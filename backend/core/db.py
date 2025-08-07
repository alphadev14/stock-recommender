# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

# Lấy URL của database từ biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL")

# Kiểm tra nếu thiếu URL thì raise lỗi rõ ràng
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Tạo engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True để debug SQL nếu cần

# Tạo session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để kế thừa trong các model
Base = declarative_base()
