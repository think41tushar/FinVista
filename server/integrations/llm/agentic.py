"""
Multi-Agent system implementation using the Agent Development Kit (ADK).
This file contains the orchestrator agent setup that coordinates the financial
transaction processing agents in the FinVista application.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the tools
from .tools import (
    save_bulk_transactions,
    update_single_transaction,
    create_relation,
    update_relation
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
        Tool(update_relation)
    ]
    
    # Define the orchestrator agent instruction
    instruction = """
    You are the FinVista Orchestrator Agent, responsible for financial transaction processing.
    
    Your responsibilities include:
    1. Processing financial transaction requests
    2. Managing transaction relationships
    3. Ensuring data consistency across the system
    
    When handling user requests:
    - For transaction updates, use the update_single_transaction tool
    - For creating relationships between entities, use the create_relation tool
    - For updating relationships, use the update_relation tool
    
    Always respond in a professional, finance-oriented manner.
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
async def process_request(request: str) -> Dict[str, Any]:
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
    user_id = "finvista_user"
    app_name = "FinVista"
    
    try:
        # Create a session with the session service
        session = await orchestrator_runner.session_service.create_session(
            app_name=app_name, 
            user_id=user_id
        )
        session_id = session.id
        logger.info(f"Created or retrieved session with ID: {session_id} for user: {user_id}")
        
        # Process the request through the orchestrator agent
        # Create a proper user content object using the types module
        user_content = types.UserContent(
            parts=[types.Part.from_text(text=request)]
        )
        
        # Run the agent asynchronously with the proper parameters
        response = None
        async for event in orchestrator_runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                response = {"response": response_text}
        
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
