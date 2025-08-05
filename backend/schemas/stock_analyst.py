class ModelPredictionOut(BaseModel):
    ticker: str
    date: date
    predicted_price: float
    trend: str
    recommendation: str
    confidence: float

    class Config:
        orm_mode = True
