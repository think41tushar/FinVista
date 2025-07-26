from fastapi import APIRouter, HTTPException
from models.user import UserIn
from services.auth_service import login_or_signup

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(data: UserIn):
    try:
        user = login_or_signup(data.email, data.password)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))