from fastapi import APIRouter, HTTPException
from models.user import UserIn
from services.auth_service import authenticate_or_register

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(data: UserIn):
    try:
        user = authenticate_or_register(data.email, data.password)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))