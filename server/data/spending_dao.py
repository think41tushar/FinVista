from .firebase_client import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

SPENDINGS = "spendings"

def create_spending(spending_data: dict):
    logger.info("Creating spending")
    now = datetime.utcnow()
    ref = db.collection(SPENDINGS).document()
    data = {
        **spending_data,
        "created_at": now,
        "updated_at": now
    }
    ref.set(data)
    return {"id": ref.id, **data}

def get_spending_by_id(spending_id: str):
    logger.info("Getting spending by id %s", spending_id)
    doc = db.collection(SPENDINGS).document(spending_id).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None

def get_all_spendings():
    logger.info("Getting all spendings")
    docs = db.collection(SPENDINGS).stream()
    return [{**d.to_dict(), "id": d.id} for d in docs]

def update_spending(spending_id: str, updates: dict):
    logger.info("Updating spending %s", spending_id)
    updates["updated_at"] = datetime.utcnow()
    db.collection(SPENDINGS).document(spending_id).update(updates)

def delete_spending(spending_id: str):
    logger.info("Deleting spending %s", spending_id)
    db.collection(SPENDINGS).document(spending_id).delete()

def bulk_create_spendings(spendings: list):
    logger.info("Bulk creating spendings")
    batch = db.batch()
    now = datetime.utcnow()
    refs = []
    for spending in spendings:
        ref = db.collection(SPENDINGS).document()
        data = {
            **spending,
            "created_at": now,
            "updated_at": now
        }
        batch.set(ref, data)
        refs.append(ref.id)
    batch.commit()
    return refs