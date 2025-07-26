from data.transaction_dao import (
    batch_create, 
    update_transaction, 
    get_all_transactions as dao_get_all_transactions,
    get_transactions_by_user_id,
    bulk_update_transactions
)
import logging

logger = logging.getLogger(__name__)

def create_transactions(txns_in):
    logger.info("Creating transactions")
    return batch_create(txns_in)

def update_single_transaction(txn_id, updates):
    logger.info("Updating transaction %s", txn_id)
    return update_transaction(txn_id, updates)

def get_all_transactions():
    logger.info("Getting all transactions")
    return dao_get_all_transactions()

def get_user_transactions(user_id: str):
    logger.info("Getting transactions for user %s", user_id)
    return get_transactions_by_user_id(user_id)

def bulk_update_transaction_data(updates: list):
    logger.info("Bulk updating transactions")
    return bulk_update_transactions(updates)