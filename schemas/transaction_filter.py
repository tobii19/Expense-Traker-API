from pydantic import BaseModel 
from datetime import date
from typing import Optional

class TransactionFilter(BaseModel):
    type :Optional[str] = None
    category_id : Optional[int] = None
    min_amount :Optional[float] = None
    max_amount :Optional[float] = None
    start_date :Optional[date] = None
    end_date :Optional[date] = None