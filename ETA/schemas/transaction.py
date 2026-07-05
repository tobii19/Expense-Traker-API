from datetime import date
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    description: str
    date: date
    type: str
    category_id: int


class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True