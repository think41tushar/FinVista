from google.adk.agents import SequentialAgent, LlmAgent
from .tools import get_all_transactions, bulk_transaction_store, update_transaction

data_cleaner = LlmAgent(
    name="data_cleaner",
    model="gemini-2.5-pro",
    description="Fetches, cleans, and stores financial transactions using MCP tools.",
    instruction="""
1. Fetch transactions via MCP.
2. Clean them (e.g., format dates, remove duplicates).
3. Store using bulk_transaction_store.
""",
    tools=[bulk_transaction_store, update_transaction]
)

data_tagger = LlmAgent(
    name="data_tagger",
    model="gemini-2.5-pro",
    description="Fetches, cleans, and stores financial transactions using MCP tools.",
    instruction="""
1. Get all transactions using get_all_transactions.
2. Analyze each transaction's description to assign a tag (e.g., 'grocery' → food, 'stock' → investment).
3. Use update_transaction to update records with appropriate tags or cleaned fields.
""",
    tools=[get_all_transactions, update_transaction]
)

pipeline = SequentialAgent(name="Initial Data Cleaning Pipeline", agents=[data_cleaner, data_tagger])