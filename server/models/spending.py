from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class SpendingIn(BaseModel):
    date: date
    title: str
    category: str

class Spending(SpendingIn):
    id: str
    created_at: datetime
    updated_at: datetime