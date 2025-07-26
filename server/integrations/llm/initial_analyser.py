import os
import logging
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.tools.function_tool import FunctionTool as Tool
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
from .tools import save_bulk_transactions, update_single_transaction, get_all_transactions, get_current_user_id
from .mcp import initialiseFiMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=API_KEY)

def create_data_cleaner_agent(mcp_tools: list):
    """Creates an agent for cleaning transaction data."""
    local_tools = [
        Tool(save_bulk_transactions),
        Tool(get_current_user_id)
    ]

    all_tools = local_tools + mcp_tools

    # Use a string model name instead of GenerativeModel instance
    return Agent(
        name="data_cleaner",
        model="gemini-2.5-flash",
        description="Cleans and stores financial transactions from MCP.",
        instruction='''
        1. Fetch 5 latest transactions from the MCP using the available tools.
        2. Fetch current user_id using get_current_user_id tool.
        3. Clean the data:
        - Convert all `date` fields to ISO 8601 datetime strings (e.g., "2025-07-24T00:00:00") or Python `datetime.datetime` objects.
        - Remove duplicates based on a combination of fields such as `date`, `amount`, and `narration`.
        - Standardize field names to match the schema: 
            `amount`, `narration`, `date`, `type`, `mode`, `balance`, `user_id`.
        - Ensure all fields are Firestore-compatible (no `datetime.date` types or unsupported objects).

        4. Store the cleaned transactions using the `save_bulk_transactions` tool.

        5. Each transaction should follow this format:
        - Use the user_id fetched in step 2.
        ```json
        [
        {
            "user_id": "user_123",
            "amount": 248.0,
            "narration": "UPI-ALIENKIND PRIVATE",
            "date": "2025-07-24T00:00:00",
            "type": "DEBIT",
            "mode": "OTHERS",
            "balance": 8242.88
        },
        {
            "user_id": "user_123",
            "amount": 6000.0,
            "narration": "UPI-KISHOR R JADHAV",
            "date": "2025-07-22T00:00:00",
            "type": "CREDIT",
            "mode": "OTHERS",
            "balance": 11560.88
        }
        ]
        ''',
        tools=all_tools
    )

def create_data_tagger_agent():
    """Creates an agent for tagging transactions."""
    tools = [
        Tool(get_all_transactions),
        Tool(update_single_transaction),
        Tool(get_current_user_id)
    ]
    return Agent(
        name="data_tagger",
        model="gemini-2.5-flash",
        description="Tags financial transactions with relevant categories.",
        instruction='''
        1. Retrieve all transactions using the get_all_transactions tool.
        2. Fetch current user_id using get_current_user_id tool.
        3. For each transaction:
           - Analyze the 'narration' and 'mode' fields to determine the most appropriate category
           - For UPI transactions, extract merchant names from the narration (e.g., 'UPI-MERCHANTNAME' → 'MERCHANTNAME')
           - Standardize transaction types to: 'CREDIT', 'DEBIT', or 'TRANSFER'
           - Add relevant tags based on transaction patterns (e.g., 'recurring', 'refund', 'online')
           - Preserve all original transaction data while adding/updating fields
        4. Update each transaction using update_single_transaction with this format:
           {
               "transaction_id": "original_id",
               "updates": {
                   "category": "standardized_category",
                   "merchant": "extracted_merchant_name",
                   "tags": ["relevant", "tags"],
                   "type": "standardized_type"
               }
           }
        5. For any ambiguous transactions, use generic categories like 'UNCATEGORIZED' rather than guessing
        6. Maintain data consistency by using consistent naming for similar transactions
        ''',
        tools=tools
    )

async def create_initial_analysis_pipeline():
    """Creates the sequential agent pipeline for initial data processing."""
    try:
        mcp_tools = await initialiseFiMCP()
    except Exception as e:
        logger.warning(f"Failed to initialize Fi MCP tools: {str(e)}. Continuing without MCP tools.")
        mcp_tools = []
        
    data_cleaner = create_data_cleaner_agent(mcp_tools)
    data_tagger = create_data_tagger_agent()
    return SequentialAgent(
        name="initial_data_pipeline",
        sub_agents=[data_cleaner, data_tagger],
        description="A pipeline to clean and tag initial financial data."
    )

# Global variables for the pipeline and runner
pipeline = None
runner = None

async def initialize_pipeline():
    """Initializes the pipeline and runner asynchronously."""
    global pipeline, runner
    if pipeline is None:
        pipeline = await create_initial_analysis_pipeline()
        session_service = InMemorySessionService()
        runner = Runner(
            agent=pipeline,
            app_name="FinVistaInitialAnalysis",
            session_service=session_service
        )
        logger.info(f"Runner object at initialize: {runner}")
        logger.info(f"Initial analysis pipeline '{pipeline.name}' initialized successfully.")
        
    # Create a session with the session service
    # Use a consistent user ID that makes sense for your application
    user_id = "finvista_user"
    session = await runner.session_service.create_session(app_name="FinVistaInitialAnalysis", user_id=user_id)
    logger.info(f"Created session with ID: {session.id} for user: {user_id}")
    
    return runner, session