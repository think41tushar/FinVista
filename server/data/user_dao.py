from .firebase_client import db
from datetime import datetime

USERS = "users"

def get_user_by_email(email: str):
    docs = db.collection(USERS).where("email", "==", email).limit(1).stream()
    for d in docs:
        data = d.to_dict(); data["id"] = d.id; return data
    return None

def create_user(name: str, email: str, hashed_password: str):
    now = datetime.utcnow()
    ref = db.collection(USERS).document()
    ref.set({
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": now,
        "updated_at": now
    })
    return { "id": ref.id, "name": name, "email": email, "hashed_password": hashed_password, "created_at": now, "updated_at": now }

def get_users_by_ids(user_ids: list):
    if not user_ids:
        return []
    users = []
    for user_id in user_ids:
        doc = db.collection(USERS).document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            users.append(data)
    return users

def update_user(user_id: str, updates: dict):
    updates["updated_at"] = datetime.utcnow()
    db.collection(USERS).document(user_id).update(updates)
    
def bulk_update_users(updates: list):
    batch = db.batch()
    now = datetime.utcnow()
    for update in updates:
        user_id = update.pop("id")
        update["updated_at"] = now
        ref = db.collection(USERS).document(user_id)
        batch.update(ref, update)
    batch.commit()