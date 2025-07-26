"""
Tools for the FinVista multi-agent system.
These tools will be used by the orchestrator agent to perform various operations.
"""
from typing import List, Dict, Any, Optional
from services.transaction_service import (
    create_transactions as save_bulk_transactions_service,
    update_single_transaction as update_single_transaction_service,
    get_all_transactions as get_all_transactions_service
)
from services.relation_service import (
    create_new_relation as create_relation_service,
    update_existing_relation as update_relation_service
)

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
        transaction_ids = save_bulk_transactions_service(transactions)
        return {
            "status": "success",
            "message": f"Successfully saved {len(transactions)} transactions.",
            "transaction_ids": transaction_ids
        }
    except Exception as e:
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
        updated_transaction = update_single_transaction_service(transaction_id, updates)
        return {
            "status": "success",
            "message": f"Successfully updated transaction {transaction_id}.",
            "transaction": updated_transaction
        }
    except Exception as e:
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
        print(f"Error getting all transactions: {e}")
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
        # Create relation data object
        relation_data = {
            "source_id": source_id,
            "target_id": target_id,
            "type": relation_type,
            "related_transactions": [source_id, target_id],  # Assuming IDs are transaction IDs
            "metadata": metadata or {}
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
            "message": f"Created relation between {source_id} and {target_id}",
            "relation_id": created_relation["id"],
            "relation": created_relation
        }
    except Exception as e:
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
        return {
            "status": "error",
            "message": str(e)
        }
    