from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RelationIn(BaseModel):
    user_id: str
    primary_transaction: str
    related_transactions: List[str]
    settlement_notes: Optional[str] = None

class Relation(RelationIn):
    id: str
    created_at: datetime
    updated_at: datetime