from datetime import date
from pydantic import BaseModel,ConfigDict

class TransactionCreate(BaseModel):
    amount: float
    description: str
    date: date
    type: str
    category_id: int

class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True) 
    
    