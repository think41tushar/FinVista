"""
Multi-Agent system implementation using the Agent Development Kit (ADK).
This file contains the orchestrator agent setup that coordinates the financial
transaction processing agents in the FinVista application.
"""

import os
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the tools
from .tools import (
    save_bulk_transactions,
    update_single_transaction,
    create_relation,
    update_relation,
    set_current_user_id,
    execute_dynamic_transaction_query
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import ADK components
from google.adk import Agent, Runner
from google.adk.tools.function_tool import FunctionTool as Tool
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
import google.generativeai as genai
from google.genai import types

# Configure Gemini API
# Get API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")
logger.info(f"GEMINI_API_KEY: {API_KEY}")
if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")
genai.configure(api_key=API_KEY)

# Create orchestrator agent
def create_orchestrator_agent():
    """Create the orchestrator agent with all tools directly attached."""
    
    # Define all tools that will be directly available to the orchestrator
    orchestrator_tools = [
        Tool(update_single_transaction),
        Tool(create_relation),
        Tool(update_relation),
        Tool(execute_dynamic_transaction_query)
    ]
    
    # Define the orchestrator agent instruction
    instruction = """
    You are the FinVista Orchestrator Agent, responsible for financial transaction processing.
    
    Your responsibilities include:
    1. Processing financial transaction requests
    2. Managing transaction relationships
    3. Ensuring data consistency across the system
    4. Answering queries about transaction data
    
    TOOL USAGE GUIDELINES:
    
    1. **update_single_transaction**: Use this tool when updating transactions that are INDEPENDENT of each other.
       - Call this tool separately for EACH referenced transaction with its specific update details
       - Use when transactions have no logical interconnection or dependency
       - Examples: Individual category updates, description changes, amount corrections for unrelated transactions
       - Parameters: transaction_id (string), updates (dict with fields to update)
    
    2. **create_relation**: Use this tool when user references MULTIPLE transactions that have logical interconnections.
       - Call when transactions are dependent on each other in some way
       - Use for transactions that have settlement possibilities
       - Use when transactions are part of the same financial flow or event
       - The system will automatically set the PRIMARY transaction as the one with the HIGHEST amount
       - Include appropriate settlement notes in the metadata
       - Examples: Transfer between accounts, loan and repayment, split bills, expense reimbursements
       - Parameters: source_id (string), target_id (string), relation_type (string), metadata (dict with "settlement_notes" key)
       
    3. **update_relation**: Use this tool to modify existing relationships between transactions.
       - Use when updating metadata, relation type, or other relationship attributes
       - Parameters: relation_id (string), updates (dict with fields to update)
       
    4. **execute_dynamic_transaction_query**: Use this tool to answer questions about transaction data.
       - Use when the user asks about spending, income, or balances over a specific time period
       - Examples: "What was my spending last week?", "How much did I earn last month?"
       - The tool will dynamically generate and execute the appropriate query
       - Parameters: query (string) - The user's natural language query about transactions
       - Will return error if query is out of scope
    
    DECISION CRITERIA:
    - If transactions are mentioned together but are logically separate → use update_single_transaction for each
    - If transactions are part of the same financial event/flow → use create_relation
    - If user mentions "settlement", "transfer", "related", "connected" → likely needs create_relation
    - If user mentions "repayment", "loan", "split", "reimbursement" → likely needs create_relation
    - If user asks about transaction amounts, spending, income for a time period → use execute_dynamic_transaction_query
    
    Always respond in a professional, finance-oriented manner and explain your actions clearly.
    
    IMPORTANT FORMATTING GUIDELINES:
    - Always use the Indian Rupee symbol (₹) when displaying monetary values
    - Format large numbers with appropriate commas according to Indian numbering system (e.g., ₹1,00,000 for one lakh)
    - Never use dollar signs ($) or other currency symbols
    """

    # Create the orchestrator agent as a regular Agent with all tools directly attached
    orchestrator_agent = Agent(
        name="finvista_orchestrator",
        description="FinVista orchestrator agent for financial transaction processing",
        instruction=instruction,
        model="gemini-2.5-pro",
        tools=orchestrator_tools
    )
    
    return orchestrator_agent

# Initialize the orchestrator agent and runner
orchestrator_agent = None
orchestrator_runner = None

# Dictionary to store active sessions by user_id with timestamps
# Format: {user_id: (session_id, timestamp)}
active_sessions = {}

# Session expiration time in seconds (default: 30 minutes)
SESSION_EXPIRATION_TIME = 30 * 60

def initialize_agents():
    """Initialize the orchestrator agent and runner."""
    global orchestrator_agent, orchestrator_runner
    
    try:
        # Create the orchestrator agent
        orchestrator_agent = create_orchestrator_agent()
        
        # Create a runner for the orchestrator agent
        # In ADK, Runner handles the execution of the agent and manages state
        session_service = InMemorySessionService()
        orchestrator_runner = Runner(
            agent=orchestrator_agent,
            app_name="FinVista",
            session_service=session_service
        )
        
        logger.info(f"Orchestrator agent '{orchestrator_agent.name}' initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize agents: {str(e)}")
        return False

# Function to process user requests through the orchestrator agent
async def process_request(request: str, user_id: str = None) -> Dict[str, Any]:
    """
    Process a user request through the orchestrator agent.
    
    Args:
        request: The user request string
        
    Returns:
        Dict containing the response and any additional information
    """
    global orchestrator_runner
    
    if orchestrator_runner is None:
        success = initialize_agents()
        if not success:
            return {
                "error": "Failed to initialize agents",
                "message": "The agent system could not be initialized"
            }
            
    # Create a session with the session service if it doesn't exist
    if user_id is None:
        user_id = "finvista_user"  # fallback for backward compatibility
    
    # Set the current user_id for tools to use
    set_current_user_id(user_id)
    app_name = "FinVista"
    
    try:
        # Check if we already have an active session for this user
        current_time = time.time()
        
        # Check if user has an active session and if it's still valid
        if user_id in active_sessions:
            session_id, timestamp = active_sessions[user_id]
            
            # Check if session has expired
            if current_time - timestamp > SESSION_EXPIRATION_TIME:
                logger.info(f"Session {session_id} for user {user_id} has expired. Creating a new one.")
                # Create a new session
                session = await orchestrator_runner.session_service.create_session(
                    app_name=app_name, 
                    user_id=user_id
                )
                session_id = session.id
                # Update the session with current timestamp
                active_sessions[user_id] = (session_id, current_time)
                logger.info(f"Created new session with ID: {session_id} for user: {user_id}")
            else:
                # Update timestamp for the existing session
                active_sessions[user_id] = (session_id, current_time)
                logger.info(f"Using existing session with ID: {session_id} for user: {user_id}")
        else:
            # Create a new session with the session service
            session = await orchestrator_runner.session_service.create_session(
                app_name=app_name, 
                user_id=user_id
            )
            session_id = session.id
            # Store the session ID and timestamp
            active_sessions[user_id] = (session_id, current_time)
            logger.info(f"Created new session with ID: {session_id} for user: {user_id}")
        
        # Process the request through the orchestrator agent
        # Create a proper user content object using the types module
        user_content = types.UserContent(
            parts=[types.Part.from_text(text=request)]
        )
        
        # Run the agent asynchronously with the proper parameters
        response = None
        try:
            async for event in orchestrator_runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content
            ):
                if event.is_final_response():
                    response_text = event.content.parts[0].text
                    response = {"response": response_text}
        except Exception as e:
            logger.error(f"Error during agent execution: {str(e)}")
            return {
                "error": "Failed to process request",
                "message": str(e)
            }
        
        return response if response else {"response": "No response generated"}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "error": "Failed to process request",
            "message": str(e)
        }

# Initialize agents when the module is imported
if __name__ != "__main__":
    logger.info("Initializing FinVista agent system...")
    initialize_agents()
