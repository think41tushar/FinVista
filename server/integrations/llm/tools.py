"""
Tools for the FinVista multi-agent system.
These tools will be used by the orchestrator agent to perform various operations.
"""
from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, date, timedelta
import re
from services.transaction_service import (
    create_transactions as save_bulk_transactions_service,
    update_single_transaction as update_single_transaction_service,
    get_all_transactions as get_all_transactions_service,
    bulk_update_transaction_data as bulk_update_transactions_service,
    get_user_transactions
)
from services.relation_service import (
    create_new_relation as create_relation_service,
    update_existing_relation as update_relation_service
)
from data.firebase_client import db

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
    

def get_current_user_id(user_id: str) -> str:
    """Get the current user ID from the request context.
    
    Args:
        user_id: The user ID to return
        
    Returns:
        The user ID
    """
    return user_id


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


# Dynamic Transaction Query Tool
def execute_dynamic_transaction_query(query: str) -> Dict[str, Any]:
    """
    Execute a dynamic transaction query based on natural language input.
    This tool enables the orchestrator to answer questions about transaction data
    by dynamically generating and executing Firestore queries.
    
    Args:
        query: Natural language query about transactions (e.g., "What was my transaction amount last week?")
        
    Returns:
        Dict containing query results or error message if query is out of scope
    """
    try:
        # Get current user ID for filtering transactions
        current_user_id = get_current_user_id()
        logger.info(f"Executing dynamic query for user {current_user_id}: {query}")
        
        # Get all user transactions as base dataset
        logger.info(f"[QUERY DEBUG] Fetching all transactions for user_id: {current_user_id}")
        all_transactions = get_user_transactions(current_user_id)
        logger.info(f"[QUERY DEBUG] Retrieved {len(all_transactions)} total transactions")
        if not all_transactions:
            return {
                "status": "success",
                "message": "No transactions found for this user.",
                "data": []
            }
        
        # Parse time period from query
        time_period, start_date, end_date = _parse_time_period(query)
        logger.info(f"[QUERY DEBUG] Parsed time period: {time_period}, start_date: {start_date}, end_date: {end_date}")
        if not time_period:
            return {
                "status": "error",
                "message": "Unable to determine time period from query."
            }
        
        # Filter transactions by date range
        logger.info(f"[QUERY DEBUG] Applying date filter: {start_date} to {end_date}")
        filtered_transactions = _filter_by_date_range(all_transactions, start_date, end_date)
        logger.info(f"[QUERY DEBUG] After date filtering: {len(filtered_transactions)} transactions remain")
        
        # Determine query type (transaction amount, spending, income, etc.)
        logger.info(f"[QUERY DEBUG] Analyzing transactions based on query type: '{query}'")
        result = _analyze_transactions_by_query(query, filtered_transactions)
        logger.info(f"[QUERY DEBUG] Analysis result type: {result.get('type', 'unknown')}")
        
        # Add context to the response
        result["time_period"] = time_period
        result["date_range"] = {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
        result["transaction_count"] = len(filtered_transactions)
        
        return {
            "status": "success",
            "message": f"Query executed successfully for {time_period}.",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error executing dynamic transaction query: {e}")
        return {
            "status": "error",
            "message": f"Unable to process this query: {str(e)}"
        }


def _parse_time_period(query: str) -> Tuple[Optional[str], Optional[date], Optional[date]]:
    """
    Parse time period from query string.
    
    Args:
        query: Natural language query
        
    Returns:
        Tuple of (time_period_description, start_date, end_date)
    """
    query = query.lower()
    today = datetime.now().date()
    
    # Check for specific time periods
    if re.search(r'\blast\s+week\b', query):
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)
        return "last week", start_date, end_date
        
    elif re.search(r'\blast\s+month\b', query):
        last_month = today.month - 1 if today.month > 1 else 12
        last_month_year = today.year if today.month > 1 else today.year - 1
        start_date = date(last_month_year, last_month, 1)
        
        # Calculate end date (last day of last month)
        if last_month == 12:
            end_date = date(last_month_year, 12, 31)
        else:
            end_date = date(last_month_year, last_month + 1, 1) - timedelta(days=1)
            
        return "last month", start_date, end_date
        
    elif re.search(r'\bthis\s+month\b', query):
        start_date = date(today.year, today.month, 1)
        # Calculate end date (last day of current month)
        if today.month == 12:
            end_date = date(today.year, 12, 31)
        else:
            end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
        return "this month", start_date, end_date
        
    elif re.search(r'\bthis\s+year\b', query):
        start_date = date(today.year, 1, 1)
        end_date = date(today.year, 12, 31)
        return "this year", start_date, end_date
        
    elif re.search(r'\blast\s+year\b', query):
        start_date = date(today.year - 1, 1, 1)
        end_date = date(today.year - 1, 12, 31)
        return "last year", start_date, end_date
    
    elif re.search(r'\btoday\b', query):
        return "today", today, today
        
    elif re.search(r'\byesterday\b', query):
        yesterday = today - timedelta(days=1)
        return "yesterday", yesterday, yesterday
    
    # If no time period found
    return None, None, None


def _filter_by_date_range(transactions: List[Dict[str, Any]], start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """
    Filter transactions by date range.
    
    Args:
        transactions: List of transaction dictionaries
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        Filtered list of transactions
    """
    if not start_date or not end_date:
        logger.info(f"[QUERY DEBUG] No date range provided, returning all {len(transactions)} transactions")
        return transactions
    
    logger.info(f"[QUERY DEBUG] Filtering {len(transactions)} transactions by date range: {start_date} to {end_date}")
    filtered = []
    date_parse_failures = 0
    date_format_issues = 0
    
    for i, txn in enumerate(transactions):
        # Handle both date string and datetime objects
        txn_date = None
        txn_id = txn.get('id', f'index_{i}')
        
        if isinstance(txn.get("date"), str):
            try:
                txn_date = datetime.fromisoformat(txn["date"]).date()
            except ValueError:
                # Try different date formats
                try:
                    txn_date = datetime.strptime(txn["date"], "%Y-%m-%d").date()
                except ValueError:
                    try:
                        # Try dd/mm/yy format
                        txn_date = datetime.strptime(txn["date"], "%d/%m/%y").date()
                    except ValueError:
                        try:
                            # Try dd/mm/yyyy format
                            txn_date = datetime.strptime(txn["date"], "%d/%m/%Y").date()
                        except ValueError:
                            date_parse_failures += 1
                            if date_parse_failures <= 3:  # Limit logging to avoid spam
                                logger.warning(f"[QUERY DEBUG] Could not parse date '{txn.get('date')}' for transaction {txn_id}")
                            continue
        elif isinstance(txn.get("date"), (datetime, date)):
            txn_date = txn["date"].date() if isinstance(txn["date"], datetime) else txn["date"]
        else:
            date_format_issues += 1
            if date_format_issues <= 3:  # Limit logging to avoid spam
                logger.warning(f"[QUERY DEBUG] Transaction {txn_id} has no date field or invalid date type: {type(txn.get('date'))}")
            continue
        
        if txn_date and start_date <= txn_date <= end_date:
            filtered.append(txn)
            if len(filtered) <= 3 or len(filtered) % 50 == 0:  # Log first few and then every 50th
                logger.info(f"[QUERY DEBUG] Transaction {txn_id} with date {txn_date} INCLUDED in results")
        else:
            if i < 5:  # Only log first few excluded transactions to avoid spam
                logger.info(f"[QUERY DEBUG] Transaction {txn_id} with date {txn_date} EXCLUDED from results")
    
    logger.info(f"[QUERY DEBUG] Date filtering complete: {len(filtered)}/{len(transactions)} transactions matched")
    if date_parse_failures > 0:
        logger.warning(f"[QUERY DEBUG] {date_parse_failures} transactions had unparseable dates")
    if date_format_issues > 0:
        logger.warning(f"[QUERY DEBUG] {date_format_issues} transactions had missing or invalid date fields")
            
    return filtered


def _analyze_transactions_by_query(query: str, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze transactions based on query type.
    
    Args:
        query: Natural language query
        transactions: List of filtered transaction dictionaries
        
    Returns:
        Analysis results based on query type
    """
    query = query.lower()
    result = {}
    
    logger.info(f"[QUERY DEBUG] Analyzing {len(transactions)} transactions for query type matching: '{query}'")
    
    # Check for different query types
    if re.search(r'transaction\s+amount|spent|spend|spending', query):
        # Calculate total spending
        logger.info(f"[QUERY DEBUG] Query matched SPENDING pattern")
        
        # Log some sample transactions for debugging
        for i, txn in enumerate(transactions[:5]):
            logger.info(f"[QUERY DEBUG] Sample transaction {i+1}: id={txn.get('id', 'unknown')}, withdrawn={txn.get('withdrawn', 0)}, deposit={txn.get('deposit', 0)}, narration={txn.get('narration', 'none')}")
        
        total_withdrawn = sum(txn.get("withdrawn", 0) for txn in transactions)
        logger.info(f"[QUERY DEBUG] Total spending (withdrawn) amount: {total_withdrawn}")
        result["total_amount"] = total_withdrawn
        result["type"] = "spending"
        
    elif re.search(r'income|deposit|earning|earned', query):
        # Calculate total income
        logger.info(f"[QUERY DEBUG] Query matched INCOME pattern")
        
        # Log some sample transactions for debugging
        for i, txn in enumerate(transactions[:5]):
            logger.info(f"[QUERY DEBUG] Sample transaction {i+1}: id={txn.get('id', 'unknown')}, deposit={txn.get('deposit', 0)}, withdrawn={txn.get('withdrawn', 0)}, narration={txn.get('narration', 'none')}")
        
        total_deposit = sum(txn.get("deposit", 0) for txn in transactions)
        logger.info(f"[QUERY DEBUG] Total income (deposit) amount: {total_deposit}")
        result["total_amount"] = total_deposit
        result["type"] = "income"
        
    elif re.search(r'balance|net|difference', query):
        # Calculate net balance (income - spending)
        logger.info(f"[QUERY DEBUG] Query matched BALANCE/NET pattern")
        
        # Log some sample transactions for debugging
        for i, txn in enumerate(transactions[:5]):
            logger.info(f"[QUERY DEBUG] Sample transaction {i+1}: id={txn.get('id', 'unknown')}, deposit={txn.get('deposit', 0)}, withdrawn={txn.get('withdrawn', 0)}, narration={txn.get('narration', 'none')}")
        
        total_deposit = sum(txn.get("deposit", 0) for txn in transactions)
        total_withdrawn = sum(txn.get("withdrawn", 0) for txn in transactions)
        net_change = total_deposit - total_withdrawn
        
        logger.info(f"[QUERY DEBUG] Total income: {total_deposit}, Total spending: {total_withdrawn}, Net change: {net_change}")
        
        result["total_amount"] = net_change
        result["deposit"] = total_deposit
        result["withdrawn"] = total_withdrawn
        result["type"] = "balance"
        
    elif re.search(r'tag|category|categorize|tagged', query):
        # Group transactions by tags
        tag_summary = {}
        for txn in transactions:
            tags = txn.get("tags", [])
            for tag in tags:
                if tag not in tag_summary:
                    tag_summary[tag] = {"count": 0, "withdrawn": 0, "deposit": 0}
                tag_summary[tag]["count"] += 1
                tag_summary[tag]["withdrawn"] += txn.get("withdrawn", 0)
                tag_summary[tag]["deposit"] += txn.get("deposit", 0)
        
        result["tag_summary"] = tag_summary
        result["type"] = "tags"
        
    else:
        # Default to showing summary stats
        total_deposit = sum(txn.get("deposit", 0) for txn in transactions)
        total_withdrawn = sum(txn.get("withdrawn", 0) for txn in transactions)
        net_change = total_deposit - total_withdrawn
        
        result["summary"] = {
            "income": total_deposit,
            "spending": total_withdrawn,
            "net_change": net_change
        }
        result["type"] = "summary"
        
    return result