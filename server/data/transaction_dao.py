from .firebase_client import db
from datetime import datetime, time, date

TXNS = "transactions"

def convert_dates_to_datetimes(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            data[key] = datetime.combine(value, time.min)
    return data

def batch_create(transactions: list):
    batch = db.batch()
    now = datetime.utcnow()
    refs = []
    for t in transactions:
        ref = db.collection(TXNS).document()
        data = t.dict()
        data = convert_dates_to_datetimes(data)  # 👈 Fix added here
        data.update({
            "closing_balance": t.deposit - t.withdrawn,
            "created_at": now,
            "updated_at": now
        })
        batch.set(ref, data)
        refs.append(ref.id)
    batch.commit()
    return refs

def update_transaction(txn_id: str, updates: dict):
    updates["updated_at"] = datetime.utcnow()
    db.collection(TXNS).document(txn_id).update(updates)
    doc = db.collection(TXNS).document(txn_id).get()
    d = doc.to_dict(); d["id"] = doc.id; return d

def get_transactions_by_ids(ids: list):
    docs = db.collection(TXNS).where(firestore.FieldPath.document_id(), "in", ids).stream()
    return [{**d.to_dict(), "id": d.id} for d in docs]