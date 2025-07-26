from .firebase_client import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

TXNS = "transactions"

def batch_create(transactions: list):
    logger.info("Creating transactions")
    batch = db.batch()
    logger.info("Batch created %s", batch)
    now = datetime.utcnow()
    logger.info("Now %s", now)
    refs = []
    logger.info("Refs %s", refs)
    for t in transactions:
        logger.info("Transaction %s", t)
        ref = db.collection(TXNS).document()
        logger.info("Ref %s", ref)
        data = t.dict()
        logger.info("Data %s", data)
        data.update({"closing_balance": t.deposit - t.withdrawn,
                     "created_at": now,
                     "updated_at": now})
        batch.set(ref, data)
        refs.append(ref.id)
    logger.info("Refs %s", refs)
    batch.commit()
    logger.info("Batch committed")
    return refs

def update_transaction(txn_id: str, updates: dict):
    logger.info("Updating transaction %s", txn_id)
    updates["updated_at"] = datetime.utcnow()
    logger.info("Updates %s", updates)
    db.collection(TXNS).document(txn_id).update(updates)
    doc = db.collection(TXNS).document(txn_id).get()
    d = doc.to_dict(); d["id"] = doc.id; logger.info("Doc %s", d); return d

def get_transactions_by_ids(ids: list):
    logger.info("Getting transactions by ids %s", ids)
    docs = db.collection(TXNS).where(firestore.FieldPath.document_id(), "in", ids).stream()
    logger.info("Docs %s", docs)
    return [{**d.to_dict(), "id": d.id} for d in docs]

def get_all_transactions():
    logger.info("Getting all transactions")
    docs = db.collection(TXNS).stream()
    logger.info("Docs %s", docs)
    return [{**d.to_dict(), "id": d.id} for d in docs]