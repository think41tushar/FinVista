"""
Tools for the FinVista multi-agent system.
These tools will be used by the orchestrator agent to perform various operations.
"""
from typing import List, Dict, Any, Optional
from services.transaction_service import (
    create_transactions as save_bulk_transactions_service,
    update_single_transaction as update_single_transaction_service,
    get_all_transactions as get_all_transactions_service,
    bulk_update_transaction_data as bulk_update_transactions_service
)
from services.relation_service import (
    create_new_relation as create_relation_service,
    update_existing_relation as update_relation_service
)

import logging
logger = logging.getLogger(__name__)

# Global variable to store current user_id for the request context
_current_user_id = None

def set_current_user_id(user_id: str):
    """Set the current user ID for the request context."""
    global _current_user_id
    _current_user_id = user_id

# Transaction Management Tools
def save_bulk_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Save multiple transactions at once using the transaction service.
    
    Args:
        transactions: List of transaction dictionaries with required fields
        
    Returns:
        Dict containing status and results
    """
    try:
        logger.info("Saving bulk transactions...")
        transaction_ids = save_bulk_transactions_service(transactions)
        logger.info("Transaction IDs: %s", transaction_ids)
        return {
            "status": "success",
            "message": f"Successfully saved {len(transactions)} transactions.",
            "transaction_ids": transaction_ids
        }
    except Exception as e:
        logger.error("Error saving bulk transactions: %s", e)
        return {
            "status": "error",
            "message": str(e)
        }

def update_single_transaction(transaction_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a single transaction by ID using the transaction service.
    
    Args:
        transaction_id: The ID of the transaction to update
        updates: Dictionary containing fields to update
        
    Returns:
        Dict containing status and updated transaction
    """
    try:
        logger.info("Updating single transaction...")
        logger.info("Transaction ID: %s", transaction_id)
        logger.info("Updates: %s", updates)
        updated_transaction = update_single_transaction_service(transaction_id, updates)
        logger.info("Updated transaction: %s", updated_transaction)
        return {
            "status": "success",
            "message": f"Successfully updated transaction {transaction_id}.",
            "transaction": updated_transaction
        }
    except Exception as e:
        logger.error("Error updating single transaction: %s", e)
        return {
            "status": "error",
            "message": str(e)
        }

def bulk_update_transactions(updates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update multiple transactions at once using the transaction service.
    
    Args:
        updates: List of update dictionaries, each containing 'transaction_id' and update fields
        
    Returns:
        Dict containing status and results
    """
    try:
        logger.info("Bulk updating transactions...")
        logger.info("Updates: %s", updates)
        results = bulk_update_transactions_service(updates)
        logger.info("Results: %s", results)
        return {
            "status": "success",
            "message": f"Successfully updated {len(updates)} transactions.",
            "results": results
        }
    except Exception as e:
        logger.error("Error bulk updating transactions: %s", e)
        return {
            "status": "error",
            "message": str(e)
        }

def get_all_transactions() -> List[Dict[str, Any]]:
    """
    Get all transactions using the transaction service.
    
    Returns:
        List of transaction dictionaries
    """
    try:
        return get_all_transactions_service()
    except Exception as e:
        logger.error("Error getting all transactions: %s", e)
        return []

# Relation Management Tools
def create_relation(source_id: str, target_id: str, relation_type: str, 
                    metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a relation between two entities.
    
    Args:
        source_id: ID of the source entity
        target_id: ID of the target entity
        relation_type: Type of relation to create
        metadata: Optional metadata for the relation
        
    Returns:
        Dict containing status and relation information
    """
    try:
        # Get the current user ID
        current_user_id = get_current_user_id()
        
        # Create relation data object according to the schema
        relation_data = {
            "user_id": current_user_id,
            "related_transactions": [source_id, target_id],  # Assuming IDs are transaction IDs
            "settlement_notes": metadata.get("settlement_notes") if metadata else None
        }
        
        # Use a Pydantic-like object for compatibility with service
        class RelationIn:
            def __init__(self, **data):
                self.__dict__.update(data)
                
            def dict(self):
                return self.__dict__
                
        rel_in = RelationIn(**relation_data)
        created_relation = create_relation_service(rel_in)
        
        return {
            "status": "success",
            "message": f"Created settlement relation between transactions {source_id} and {target_id}",
            "relation_id": created_relation["id"],
            "relation": created_relation
        }
    except Exception as e:
        logger.error("Error creating relation: %s", e)
        return {
            "status": "error",
            "message": str(e)
        }
    

def update_relation(relation_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing relation.
    
    Args:
        relation_id: ID of the relation to update
        updates: Dictionary containing fields to update
        
    Returns:
        Dict containing status and updated relation
    """
    try:
        updated_relation = update_relation_service(relation_id, updates)
        return {
            "status": "success",
            "message": f"Updated relation {relation_id}",
            "relation": updated_relation
        }
    except Exception as e:
        logger.error("Error updating relation: %s", e)
        return {
            "status": "error",
            "message": str(e)
        }
    

def get_current_user_id() -> str:
    """Get the current user ID from the request context."""
    global _current_user_id
    if _current_user_id is not None:
        return _current_user_id
    # Fallback to hardcoded value for backward compatibility
    return "5qQv5bR5BB4BqTYj0Qna"


def get_sample_transactions() -> List[Dict[str, Any]]:
    """
    Returns the sample transaction data used for initializing the database.
    This provides a consistent set of transaction examples for testing and development.
    
    Returns:
        List of sample transaction dictionaries
    """
    try:
        logger.info("Fetching sample transactions...")
        from scripts.init_database import SAMPLE_TRANSACTIONS
        return SAMPLE_TRANSACTIONS
    except Exception as e:
        logger.error("Error fetching sample transactions: %s", e)
        return {
            "status": "error",
            "message": f"Error fetching sample transactions: {str(e)}"
        }