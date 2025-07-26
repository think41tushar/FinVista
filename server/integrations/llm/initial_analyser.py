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
from .tools import save_bulk_transactions, update_single_transaction, get_all_transactions
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
        Tool(save_bulk_transactions)
    ]

    all_tools = local_tools + mcp_tools

    # Use a string model name instead of GenerativeModel instance
    return Agent(
        name="data_cleaner",
        model="gemini-2.5-flash",
        description="Cleans and stores financial transactions from MCP.",
        instruction='''
        1. Fetch transactions from the MCP using the available tools.

        2. Clean the data:
        - Convert all `date` fields to ISO 8601 datetime strings (e.g., "2025-07-24T00:00:00") or Python `datetime.datetime` objects.
        - Remove duplicates based on a combination of fields such as `date`, `amount`, and `narration`.
        - Standardize field names to match the schema: 
            `amount`, `narration`, `date`, `type`, `mode`, `balance`, `user_id`.
        - Ensure all fields are Firestore-compatible (no `datetime.date` types or unsupported objects).

        3. Store the cleaned transactions using the `save_bulk_transactions` tool.

        4. Each transaction should follow this format:
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
        Tool(update_single_transaction)
    ]
    return Agent(
        name="data_tagger",
        model="gemini-2.5-flash",
        description="Tags financial transactions with relevant categories.",
        instruction='''
        1. Retrieve all transactions using the get_all_transactions tool.
        2. Analyze the description of each transaction to determine a suitable tag (e.g., 'food', 'investment').
        3. Update each transaction with its new tag using the update_single_transaction tool.
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