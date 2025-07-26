from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

class TransactionIn(BaseModel):
    user_id: str
    date: date
    narration: str
    withdrawn: float = 0.0
    deposit: float = 0.0
    type: str
    tags: List[str] = []
    remarks: Optional[str] = None
    processed: str = ""

class Transaction(TransactionIn):
    id: str
    closing_balance: float
    created_at: datetime
    updated_at: datetime