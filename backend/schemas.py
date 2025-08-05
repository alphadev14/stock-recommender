from pydantic import BaseModel

class FetchRequest(BaseModel):
    symbol: str
    start: str
    end: str