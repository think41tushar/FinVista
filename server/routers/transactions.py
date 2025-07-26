from fastapi import APIRouter, HTTPException
from typing import List
from models.transaction import TransactionIn
from services.transaction_service import (
    create_transactions, 
    update_single_transaction,
    get_user_transactions,
    bulk_update_transaction_data
)

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

@router.get("/user/{user_id}")
def get_by_user_id(user_id: str):
    try:
        return get_user_transactions(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/bulk-update")
def bulk_update(updates: List[dict]):
    try:
        bulk_update_transaction_data(updates)
        return {"message": "Transactions updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))