from data.relation_dao import (
    create_relation, 
    update_relation, 
    get_relation,
    get_relations_by_user_id,
    get_all_relations,
    delete_relation
)
from data.transaction_dao import get_transactions_by_ids
import logging

logger = logging.getLogger(__name__)

def calculate_primary_transaction(transaction_ids: list):
    """Calculate which transaction should be primary based on largest amount"""
    if not transaction_ids:
        return None
    
    txns = get_transactions_by_ids(transaction_ids)
    if not txns:
        return None
    
    # Find transaction with max absolute amount
    def get_amount(t): 
        return max(t.get("deposit", 0), t.get("withdrawn", 0))
    
    largest = max(txns, key=get_amount)
    return largest["id"]

def create_new_relation(rel_in):
    logger.info("Creating new relation")
    data = rel_in.dict()
    
    # Calculate primary transaction
    primary_id = calculate_primary_transaction(data.get("related_transactions", []))
    if primary_id:
        data["primary_transaction"] = primary_id
    
    return create_relation(data)

def update_existing_relation(rel_id, rel_updates):
    logger.info("Updating existing relation %s", rel_id)
    
    # Get current relation
    rel = get_relation(rel_id)
    if not rel:
        raise Exception("Relation not found")
    
    # If related_transactions changed, recalculate primary transaction
    if "related_transactions" in rel_updates:
        new_related = rel_updates["related_transactions"]
        primary_id = calculate_primary_transaction(new_related)
        if primary_id:
            rel_updates["primary_transaction"] = primary_id
    
    return update_relation(rel_id, rel_updates)

def get_relation_by_id(rel_id: str):
    logger.info("Getting relation %s", rel_id)
    return get_relation(rel_id)

def get_user_relations(user_id: str):
    logger.info("Getting relations for user %s", user_id)
    return get_relations_by_user_id(user_id)

def list_all_relations():
    logger.info("Getting all relations")
    return get_all_relations()

def remove_relation(rel_id: str):
    logger.info("Deleting relation %s", rel_id)
    return delete_relation(rel_id)

def add_transaction_to_relation(rel_id: str, transaction_id: str):
    """Add a transaction to an existing relation and recalculate primary"""
    logger.info("Adding transaction %s to relation %s", transaction_id, rel_id)
    
    rel = get_relation(rel_id)
    if not rel:
        raise Exception("Relation not found")
    
    # Add transaction to related transactions if not already present
    related_transactions = rel.get("related_transactions", [])
    if transaction_id not in related_transactions:
        related_transactions.append(transaction_id)
        
        # Recalculate primary transaction
        primary_id = calculate_primary_transaction(related_transactions)
        
        updates = {
            "related_transactions": related_transactions,
            "primary_transaction": primary_id
        }
        
        return update_relation(rel_id, updates)
    
    return rel