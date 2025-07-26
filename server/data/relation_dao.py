from .firebase_client import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

RELS = "relations"

def create_relation(data: dict):
    logger.info("Creating relation")
    now = datetime.utcnow()
    ref = db.collection(RELS).document()
    data.update({"created_at": now, "updated_at": now})
    ref.set(data)
    return {**data, "id": ref.id}

def update_relation(rel_id: str, updates: dict):
    logger.info("Updating relation %s", rel_id)
    updates["updated_at"] = datetime.utcnow()
    db.collection(RELS).document(rel_id).update(updates)
    doc = db.collection(RELS).document(rel_id).get()
    if doc.exists:
        d = doc.to_dict()
        d["id"] = doc.id
        return d
    return None

def get_relation(rel_id: str):
    logger.info("Getting relation %s", rel_id)
    doc = db.collection(RELS).document(rel_id).get()
    if doc.exists:
        d = doc.to_dict()
        d["id"] = doc.id
        return d
    return None

def get_relations_by_user_id(user_id: str):
    logger.info("Getting relations by user_id %s", user_id)
    docs = db.collection(RELS).where("user_id", "==", user_id).stream()
    return [{**d.to_dict(), "id": d.id} for d in docs]

def get_all_relations():
    logger.info("Getting all relations")
    docs = db.collection(RELS).stream()
    return [{**d.to_dict(), "id": d.id} for d in docs]

def delete_relation(rel_id: str):
    logger.info("Deleting relation %s", rel_id)
    db.collection(RELS).document(rel_id).delete()