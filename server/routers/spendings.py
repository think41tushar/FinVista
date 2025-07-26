from fastapi import APIRouter, HTTPException
from typing import List
from models.spending import SpendingIn
from services.spending_service import (
    create_new_spending,
    get_spending,
    list_all_spendings,
    update_spending_data,
    remove_spending,
    create_multiple_spendings
)

router = APIRouter(prefix="/spendings")

@router.post("/")
def create(spending: SpendingIn):
    try:
        return create_new_spending(spending.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bulk")
def create_multiple(spendings: List[SpendingIn]):
    try:
        spending_dicts = [spending.dict() for spending in spendings]
        return create_multiple_spendings(spending_dicts)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{spending_id}")
def get_by_id(spending_id: str):
    try:
        spending = get_spending(spending_id)
        if not spending:
            raise HTTPException(status_code=404, detail="Spending not found")
        return spending
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all():
    try:
        return list_all_spendings()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{spending_id}")
def update(spending_id: str, updates: dict):
    try:
        update_spending_data(spending_id, updates)
        return {"message": "Spending updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{spending_id}")
def delete(spending_id: str):
    try:
        remove_spending(spending_id)
        return {"message": "Spending deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))