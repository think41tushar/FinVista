from fastapi import APIRouter, HTTPException
from typing import List
from models.user import UserIn
from services.auth_service import authenticate_or_register
from data.user_dao import get_users_by_ids, update_user, bulk_update_users

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(data: UserIn):
    try:
        user = authenticate_or_register(data.name, data.email, data.password)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/bulk-fetch")
def bulk_fetch_users(user_ids: List[str]):
    try:
        return get_users_by_ids(user_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/{user_id}")
def update_single_user(user_id: str, updates: dict):
    try:
        update_user(user_id, updates)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/bulk-update")
def bulk_update_user_data(updates: List[dict]):
    try:
        bulk_update_users(updates)
        return {"message": "Users updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))