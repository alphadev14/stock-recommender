from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import stock  # Router module

app = FastAPI(title="Stock Recommender API", version="1.0")

# Cho phép gọi từ frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def read_root():
    return {"message": "Welcome to Stock Recommender API"}

# Router include
app.include_router(stock.router)
