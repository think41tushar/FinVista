from .firebase_client import db
from datetime import datetime

RELS = "relations"

def create_relation(data: dict):
    now = datetime.utcnow()
    ref = db.collection(RELS).document()
    data.update({"created_at": now, "updated_at": now})
    ref.set(data)
    return {**data, "id": ref.id}

def update_relation(rel_id: str, updates: dict):
    updates["updated_at"] = datetime.utcnow()
    db.collection(RELS).document(rel_id).update(updates)
    doc = db.collection(RELS).document(rel_id).get()
    d = doc.to_dict(); d["id"] = doc.id; return d

def get_relation(rel_id: str):
    doc = db.collection(RELS).document(rel_id).get()
    d = doc.to_dict(); d["id"] = doc.id; return d