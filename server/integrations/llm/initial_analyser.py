import os
import logging
import os
import logging
from google.adk import Agent, Tool, Runner
from google.adk.agents import SequentialAgent
from google.genai import GenerativeModel
import google.generativeai as genai
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
        Tool(
            func=save_bulk_transactions,
            name="save_bulk_transactions",
            description="Stores cleaned financial transactions."
        )
    ]

    all_tools = local_tools + mcp_tools

    model = GenerativeModel("gemini")
    return Agent(
        name="data_cleaner",
        model=model,
        description="Cleans and stores financial transactions from MCP.",
        instruction='''
        1. Fetch transactions from the MCP using the available tools.
        2. Clean the data (format dates, remove duplicates).
        3. Store the cleaned data using the save_bulk_transactions tool.
        ''',
        tools=all_tools
    )

def create_data_tagger_agent():
    """Creates an agent for tagging transactions."""
    tools = [
        Tool(
            func=get_all_transactions,
            name="get_all_transactions",
            description="Retrieves all financial transactions."
        ),
        Tool(
            func=update_single_transaction,
            name="update_single_transaction",
            description="Updates a transaction with a tag."
        )
    ]
    model = GenerativeModel("gemini")
    return Agent(
        name="data_tagger",
        model=model,
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
    mcp_tools = await initialiseFiMCP()
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
        runner = Runner(agent=pipeline, app_name="FinVistaInitialAnalysis")
        logger.info(f"Initial analysis pipeline '{pipeline.name}' initialized successfully.")