from .firebase_client import db
from datetime import datetime, time, date
import logging

logger = logging.getLogger(__name__)

TXNS = "transactions"

def convert_dates_to_datetimes(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            data[key] = datetime.combine(value, time.min)
    return data

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
        # Check if t is already a dictionary or has a dict() method
        if isinstance(t, dict):
            data = t
        elif hasattr(t, 'dict') and callable(t.dict):
            data = t.dict()
        else:
            # Try to convert to dictionary using __dict__ if available
            data = vars(t) if hasattr(t, '__dict__') else {}
        
        logger.info("Data %s", data)
        
        # Convert any date objects to datetime
        data = convert_dates_to_datetimes(data)
        
        # Safely access deposit and withdrawn values
        deposit = data.get('deposit', 0)
        withdrawn = data.get('withdrawn', 0)
        
        data.update({
            "closing_balance": deposit - withdrawn,
            "created_at": now,
            "updated_at": now
        })
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
    transactions = []
    for doc_id in ids:
        doc = db.collection(TXNS).document(doc_id).get()
        if doc.exists:
            transaction_data = doc.to_dict()
            transaction_data["id"] = doc.id
            transactions.append(transaction_data)
    logger.info("Found %d transactions", len(transactions))
    return transactions

def get_all_transactions():
    logger.info("Getting all transactions")
    docs = db.collection(TXNS).stream()
    logger.info("Docs %s", docs)
    return [{**d.to_dict(), "id": d.id} for d in docs]

def get_transactions_by_user_id(user_id: str):
    logger.info("Getting transactions by user_id %s", user_id)
    docs = db.collection(TXNS).where("user_id", "==", user_id).stream()
    return [{**d.to_dict(), "id": d.id} for d in docs]

def bulk_update_transactions(updates: list):
    logger.info("Bulk updating transactions")
    batch = db.batch()
    now = datetime.utcnow()
    for update in updates:
        # Handle both id and transaction_id formats
        if "id" in update:
            txn_id = update.pop("id")
        elif "transaction_id" in update:
            txn_id = update.pop("transaction_id")
            # If updates are nested inside an 'updates' field, extract them
            if "updates" in update:
                update = update["updates"]
        else:
            logger.error(f"Missing ID field in update: {update}")
            continue
            
        update["updated_at"] = now
        ref = db.collection(TXNS).document(txn_id)
        batch.update(ref, update)
    batch.commit()
    logger.info("Bulk update completed")