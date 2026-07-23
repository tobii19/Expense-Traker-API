from pydantic import BaseModel
from typing import Optional
from datetime import date
from typing import List, Optional

class TransactionFilter(BaseModel):
    type: Optional[str] = None
    category_id: Optional[int] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    sort_by: Optional[str] = None
    order: Optional[str] = "asc"
    