# 📦 Stock Recommender Backend

This is the **backend service** for the Stock Recommender System. It provides APIs for:

- Fetching and storing raw stock data
- Storing financial indicators and model predictions
- Serving data to the frontend dashboard and machine learning models

---

## 🚀 Tech Stack

- **Python 3.10+**
- **FastAPI** – High-performance API framework
- **SQLAlchemy** – ORM for PostgreSQL
- **Pydantic** – Request/Response validation
- **PostgreSQL** – Relational database for raw and structured data
- **MongoDB** _(planned)_ – For unstructured AI-related outputs
- **Redis** _(planned)_ – For caching frontend queries
- **Docker** _(optional)_ – Deployment and testing

---

## 📁 Project Structure

```
backend/
├── main.py                # FastAPI entry point
├── database.py           # PostgreSQL connection setup
├── models.py             # SQLAlchemy ORM models
├── init_db.py            # Create tables from models
│
├── api/                  # FastAPI route definitions
│   └── v1/               # API versioning (v1)
│       └── stock.py      # Routes for stock data
│
├── schemas/              # Pydantic models for validation
│   └── stock.py
│
├── crud/                 # Database operations (select, insert, update)
│   └── stock.py
│
├── services/             # Business logic layer
│   └── stock.py
│
├── core/                 # Configurations (env, settings)
│   └── config.py
│
├── utils/                # Utility helpers
│   └── helper.py
│
├── .env                  # Environment variables
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-username/stock-recommender.git
cd stock-recommender/backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup environment variables

Create a `.env` file:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock
DB_USER=postgres
DB_PASS=your_password
```

### 4. Create tables in PostgreSQL

```bash
python init_db.py
```

### 5. Run FastAPI server

```bash
uvicorn main:app --reload --port 8000
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.

---

## 🔌 API Overview

### `POST /api/v1/fetch-data/`

- Fetch stock data from VNStock
- Compute technical indicators
- Save to PostgreSQL

### `GET /api/v1/prices/{ticker}` _(planned)_

- Get historical prices of a ticker

### `GET /api/v1/info/{ticker}` _(planned)_

- Get company info

### `GET /api/v1/predict/{ticker}` _(planned)_

- Get predicted price and recommendation

---

## 🧠 AI / Analytics Modules (Planned)

- Training LSTM/Transformer models with historical data
- Predict future prices, trends, and confidence scores
- Store results in `stock_analyst.model_predictions`
- Notify via Discord or dashboard alerts

---

## 🛠️ Dev Tips

- Use [DBeaver](https://dbeaver.io/) to inspect PostgreSQL tables
- Use `alembic` for future schema migrations
- Use `.env` and `python-dotenv` for secure credentials

---

## 🧑‍💻 Author & Maintainer

**Alpha** – Data Engineer / AI Stock Explorer

---

## 📄 License

MIT License – Free to use, modify, and distribute.
