import os
import logging
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.tools.function_tool import FunctionTool as Tool
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
import google.generativeai as genai

# Custom exception for pipeline termination
class MCPFailureException(Exception):
    """Exception raised when MCP fails and pipeline should terminate."""
    def __init__(self, message, mcp_response=None):
        super().__init__(message)
        self.mcp_response = mcp_response

# Load environment variables from .env file
load_dotenv()
from .tools import save_bulk_transactions, bulk_update_transactions, get_all_transactions, get_current_user_id, get_sample_transactions
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

def create_transaction_fetcher_agent(mcp_tools: list):
    """Agent 1: Fetches transactions using gemini-2.5-flash."""
    return Agent(
        name="transaction_fetcher",
        model="gemini-2.5-flash",
        description="Fetches financial transactions from MCP or sample data.",
        instruction='''
        1. Try to fetch 5 latest transactions from the MCP using the available MCP tools ( specifically use fetch_bank_transactions tool only ).
        2. If the MCP fails or no MCP tools are available.
        3. Return the raw transaction data without any processing.
        4. Ensure the data is properly formatted for the next agent in the pipeline.
        
        Output the fetched transactions in a structured format that can be easily processed by subsequent agents.
        ''',
        tools=mcp_tools
    )

def create_user_id_fetcher_agent():
    """Agent 2: Fetches current user ID using gemini-2.5-flash."""
    return Agent(
        name="user_id_fetcher",
        model="gemini-2.5-flash",
        description="Fetches the current user ID for transaction processing.",
        instruction='''
        IMPORTANT: Check the previous agent's response first.
        
        1. If the previous agent's response starts with "MCP_FAILURE:", 
           - IMMEDIATELY stop and return: "PIPELINE_TERMINATED: MCP failed in previous step"
           - Do NOT execute any tools
        
        2. If the previous agent succeeded:
           - Fetch the current user_id using the get_current_user_id tool
           - Return the user_id in a clear format for use by subsequent agents
           - This user_id will be used to associate all transactions with the correct user
        ''',
        tools=[Tool(get_current_user_id)]
    )

def create_data_cleaner_agent():
    """Agent 3: Cleans and stores transaction data using gemini-2.5-pro."""
    return Agent(
        name="data_cleaner",
        model="gemini-2.5-pro",
        description="Cleans transaction data and stores it in the database.",
        instruction='''
        IMPORTANT: Check previous agents' responses for termination signals.
        
        1. If any previous agent's response contains "MCP_FAILURE:" or "PIPELINE_TERMINATED:":
           - IMMEDIATELY stop and return: "PIPELINE_TERMINATED: Previous step failed"
           - Do NOT execute any tools or processing
        
        2. If previous agents succeeded, you will receive:
           - Raw transaction data from the transaction_fetcher agent
           - User ID from the user_id_fetcher agent
        
        3. Clean the transaction data:
           - Convert all `date` fields to ISO 8601 datetime strings (e.g., "2025-07-24T00:00:00") or Python `datetime.datetime` objects.
           - Remove duplicates based on a combination of fields such as `date`, `amount`, and `narration`.
           - Standardize field names to match the schema: `amount`, `narration`, `date`, `type`, `mode`, `balance`, `user_id`.
           - Ensure all fields are Firestore-compatible (no `datetime.date` types or unsupported objects).
           - Add the user_id to each transaction record.

        4. Store the cleaned transactions using the `save_bulk_transactions` tool. This is mandatory - do not proceed without calling this tool.

        5. Each transaction should follow this format:
        ```json
        [
            {
                "user_id": "user_123",
                "amount": 248.0,
                "narration": "UPI-ALIENKIND PRIVATE",
                "date": "2025-07-24T00:00:00",
                "type": "DEBIT",
                "mode": "OTHERS",
                "balance": 8242.88,
                "processed": "unprocessed"
            },
            {
                "user_id": "user_123",
                "amount": 6000.0,
                "narration": "UPI-KISHOR R JADHAV",
                "date": "2025-07-22T00:00:00",
                "type": "CREDIT",
                "mode": "OTHERS",
                "balance": 11560.88,
                "processed": "unprocessed"
            }
        ]
        ```
        
        6. Confirm successful storage and pass the transaction count to the next agent.
        7. Strictly add "processed": "unprocessed" to each transaction.
        ''',
        tools=[Tool(save_bulk_transactions)]
    )

def create_data_tagger_agent():
    """Agent 4: Tags transactions with categories using gemini-2.5-pro."""
    return Agent(
        name="data_tagger",
        model="gemini-2.5-pro",
        description="Tags financial transactions with relevant categories and metadata.",
        instruction='''
        IMPORTANT: Check previous agents' responses for termination signals.
        
        1. If any previous agent's response contains "MCP_FAILURE:" or "PIPELINE_TERMINATED:":
           - IMMEDIATELY stop and return: "PIPELINE_TERMINATED: Previous step failed"
           - Do NOT execute any tools or processing
        
        2. If previous agents succeeded, you will receive confirmation that transactions have been cleaned and stored.
        
        3. Retrieve all transactions using the get_all_transactions tool.
        4. Fetch current user_id using get_current_user_id tool for verification.
        
        5. For each transaction, perform intelligent analysis:
           - Analyze the 'narration' and 'mode' fields to determine the most appropriate category
           - For UPI transactions, extract merchant names from the narration (e.g., 'UPI-MERCHANTNAME' → 'MERCHANTNAME')
           - Standardize transaction types to: 'CREDIT', 'DEBIT', or 'TRANSFER'
           - Add relevant tags based on transaction patterns (e.g., 'recurring', 'refund', 'online', 'grocery', 'fuel', 'entertainment')
           - Categorize transactions into meaningful groups (e.g., 'FOOD_DINING', 'TRANSPORTATION', 'UTILITIES', 'SHOPPING', 'INCOME', etc.)
           - Preserve all original transaction data while adding/updating fields
        
        6. Update all transactions using bulk_update_transactions tool. Use the original transaction id from get_all_transactions. 
           Update format:
           ```json
           [
               {
                   "transaction_id": "original_id",
                   "updates": {
                       "category": "standardized_category",
                       "merchant": "extracted_merchant_name",
                       "tags": ["relevant", "tags"],
                       "type": "standardized_type",
                       "processed": "analyzed"
                   }
               }
           ]
           ```
        
        7. For ambiguous transactions, use 'UNCATEGORIZED' rather than guessing.
        8. Maintain consistency by using standard naming for similar transactions.
        9. Directly return the return without any additional summarization and text after the response from bulk_update_transactions tool.
        10. Strictly add "processed": "analyzed" to each transaction.
        ''',
        tools=[
            Tool(get_all_transactions),
            Tool(bulk_update_transactions),
            Tool(get_current_user_id)
        ]
    )

async def create_four_agent_pipeline():
    """Creates the sequential agent pipeline with 4 specialized agents."""
    try:
        mcp_tools = await initialiseFiMCP()
        logger.info(f"Successfully initialized {len(mcp_tools)} MCP tools")
    except Exception as e:
        logger.warning(f"Failed to initialize Fi MCP tools: {str(e)}. Continuing without MCP tools.")
        mcp_tools = []
        
    # Create all 4 agents
    transaction_fetcher = create_transaction_fetcher_agent(mcp_tools)
    user_id_fetcher = create_user_id_fetcher_agent()
    data_cleaner = create_data_cleaner_agent()
    data_tagger = create_data_tagger_agent()
    
    # Create sequential pipeline
    return SequentialAgent(
        name="four_agent_data_pipeline",
        sub_agents=[transaction_fetcher, user_id_fetcher, data_cleaner, data_tagger],
        description="A 4-agent pipeline: fetch transactions (flash), fetch user ID (flash), clean & store data (pro), tag transactions (pro)."
    )

# Global variables for the pipeline and runner
pipeline = None
runner = None

async def initialize_pipeline():
    """Initializes the 4-agent pipeline and runner asynchronously."""
    global pipeline, runner
    if pipeline is None:
        pipeline = await create_four_agent_pipeline()
        session_service = InMemorySessionService()
        runner = Runner(
            agent=pipeline,
            app_name="FinVistaFourAgentAnalysis",
            session_service=session_service
        )
        logger.info(f"Runner object at initialize: {runner}")
        logger.info(f"Four-agent pipeline '{pipeline.name}' initialized successfully.")
        logger.info("Agent distribution:")
        logger.info("  - transaction_fetcher: gemini-2.5-flash (with MCP failure detection)")
        logger.info("  - user_id_fetcher: gemini-2.5-flash (with termination check)") 
        logger.info("  - data_cleaner: gemini-2.5-pro (with termination check)")
        logger.info("  - data_tagger: gemini-2.5-pro (with termination check)")
        
    # Create a session with the session service
    user_id = "finvista_user"
    session = await runner.session_service.create_session(
        app_name="FinVistaFourAgentAnalysis", 
        user_id=user_id
    )
    logger.info(f"Created session with ID: {session.id} for user: {user_id}")
    
    return runner, session

async def run_pipeline_with_error_handling():
    """Runs the pipeline with proper error handling for MCP failures."""
    try:
        runner, session = await initialize_pipeline()
        
        # Start the pipeline
        response = await runner.run(
            session_id=session.id,
            input_text="Start the financial data processing pipeline"
        )
        
        # Check if MCP failed in the first step
        if "MCP_FAILURE:" in response:
            logger.error("Pipeline terminated due to MCP failure")
            return {
                "status": "failed",
                "reason": "MCP_FAILURE",
                "response": response,
                "terminated_at": "transaction_fetcher"
            }
        elif "PIPELINE_TERMINATED:" in response:
            logger.error("Pipeline terminated in later step")
            return {
                "status": "failed", 
                "reason": "PIPELINE_TERMINATED",
                "response": response
            }
        else:
            logger.info("Pipeline completed successfully")
            return {
                "status": "success",
                "response": response
            }
            
    except Exception as e:
        logger.error(f"Pipeline execution failed with exception: {str(e)}")
        return {
            "status": "error",
            "reason": "EXCEPTION",
            "error": str(e)
        }

# Alternative function if you want to run individual agents
async def run_individual_agent(agent_name: str, input_data=None):
    """Run a specific agent individually for testing purposes."""
    global pipeline
    if pipeline is None:
        await initialize_pipeline()
    
    # Find the specific agent
    for agent in pipeline.sub_agents:
        if agent.name == agent_name:
            logger.info(f"Running individual agent: {agent_name}")
            # You can add logic here to run the agent individually if needed
            return agent
    
    logger.error(f"Agent '{agent_name}' not found in pipeline")
    return None