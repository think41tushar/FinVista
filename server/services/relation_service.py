from data.relation_dao import create_relation, update_relation, get_relation
from data.transaction_dao import get_transactions_by_ids

def create_new_relation(rel_in):
    return create_relation(rel_in.dict())

def update_existing_relation(rel_id, rel_updates):
    # if related_transactions changed, recalc primary if needed
    rel = get_relation(rel_id)
    new_related = rel_updates.get("related_transactions", rel["related_transactions"])
    txns = get_transactions_by_ids(new_related)
    # find txn with max absolute amount
    def amount(t): return max(t.get("deposit",0), t.get("withdrawn",0))
    largest = max(txns, key=amount)
    rel_updates["primary_transaction"] = largest["id"]
    return update_relation(rel_id, rel_updates)