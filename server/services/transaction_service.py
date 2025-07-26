from data.transaction_dao import batch_create, update_transaction

def create_transactions(txns_in):
    return batch_create(txns_in)

def update_single_transaction(txn_id, updates):
    return update_transaction(txn_id, updates)