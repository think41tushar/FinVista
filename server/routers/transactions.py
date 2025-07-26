from fastapi import APIRouter, HTTPException
from typing import List
from models.transaction import TransactionIn
from services.transaction_service import create_transactions, update_single_transaction

router = APIRouter(prefix="/transactions")

@router.post("/", response_model=List[str])
def create_multiple(txns: List[TransactionIn]):
    return create_transactions(txns)

@router.put("/{txn_id}")
def update(txn_id: str, updates: dict):
    try:
        return update_single_transaction(txn_id, updates)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))