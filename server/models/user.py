from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserIn(BaseModel):
    name: Optional[str] = "Alex"
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    updated_at: datetime