from .firebase_client import db
from datetime import datetime

USERS = "users"

def get_user_by_email(email: str):
    docs = db.collection(USERS).where("email", "==", email).limit(1).stream()
    for d in docs:
        data = d.to_dict(); data["id"] = d.id; return data
    return None

def create_user(email: str, hashed_password: str):
    now = datetime.utcnow()
    ref = db.collection(USERS).document()
    ref.set({
        "email": email,
        "hashed_password": hashed_password,
        "created_at": now,
        "updated_at": now
    })
    return { "id": ref.id, "email": email, "hashed_password": hashed_password, "created_at": now, "updated_at": now }