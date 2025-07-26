transaction_db: Dict[str, Dict] = {}

async def bulk_transaction_store(transactions: List[Dict]) -> str:
    for tx in transactions:
        tx_id = tx.get("id", str(len(transaction_db)))
        transaction_db[tx_id] = tx  # Store cleaned transaction
    return f"Stored {len(transactions)} transactions."

async def update_transaction(transaction_id: str, updates: Dict) -> str:
    if transaction_id in transaction_db:
        transaction_db[transaction_id].update(updates)
        return f"Updated transaction {transaction_id}."
    return "Transaction not found."

async def calculate_spending_by_tag(tag: str) -> str:
    total = sum(tx.get("amount", 0) for tx in transaction_db.values() if tx.get("tag") == tag)
    return f"Total spending for tag '{tag}': {total}"

async def get_all_transactions() -> List[Dict]:
    return list(transaction_db.values())
    