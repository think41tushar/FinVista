from data.transaction_dao import batch_create, update_transaction, get_all_transactions
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
    return get_all_transactions()