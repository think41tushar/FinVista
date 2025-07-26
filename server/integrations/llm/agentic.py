"""
Multi-Agent system implementation using the Agent Development Kit (ADK).
This file contains the orchestrator agent setup that coordinates the financial
transaction processing agents in the FinVista application.
"""

import os
import logging
from typing import Dict, Any, List, Optional

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
from google.adk import Agent, Tool, Runner
from google.adk.agents import SequentialAgent
from google.genai import GenerativeModel
import google.generativeai as genai

# Configure Gemini API
# Get API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")
genai.configure(api_key=API_KEY)

# Create transaction agent
def create_transaction_agent():
    """Create an agent specialized in transaction management."""
    # Define transaction tools
    transaction_tools = [
        Tool(
            func=save_bulk_transactions,
            name="save_bulk_transactions",
            description="Save multiple transactions at once. Input should be a list of transaction objects."
        ),
        Tool(
            func=update_single_transaction,
            name="update_single_transaction",
            description="Update a single transaction by ID. Input should be the transaction ID and the fields to update."
        ),
    ]
    
    # Create a Gemini model for the agent
    transaction_model = GenerativeModel("gemini")  # Using standard Gemini model instead of Pro
    
    # Create transaction agent using ADK
    transaction_agent = Agent(
        name="transaction_agent",
        description="Manages financial transaction operations",
        instruction="You are a Transaction Management Agent. Your role is to process and manage financial transactions.\n"
                    "You can save multiple transactions at once or update individual transactions.\n"
                    "Always respond in a professional manner suitable for financial operations.",
        model=transaction_model,  # Use the actual Gemini model instance
        tools=transaction_tools
    )
    
    return transaction_agent

# Create relation agent
def create_relation_agent():
    """Create an agent specialized in relation management."""
    # Define relation tools
    relation_tools = [
        Tool(
            func=create_relation,
            name="create_relation",
            description="Create a relation between two entities. Input should be source ID, target ID, relation type, and optional metadata."
        ),
        Tool(
            func=update_relation,
            name="update_relation",
            description="Update an existing relation. Input should be the relation ID and the fields to update."
        )
    ]
    
    # Create a Gemini model for the agent
    relation_model = GenerativeModel("gemini")  # Using standard Gemini model instead of Pro
    
    # Create relation agent using ADK
    relation_agent = Agent(
        name="relation_agent",
        description="Manages relationships between financial entities",
        instruction="You are a Relation Management Agent. Your role is to establish and update relationships "
                    "between financial entities.\n"
                    "You can create new relations or update existing ones.\n"
                    "Always respond in a professional manner suitable for financial operations.",
        model=relation_model,  # Use the actual Gemini model instance
        tools=relation_tools
    )
    
    return relation_agent

# Create orchestrator agent
def create_orchestrator_agent():
    """Create the orchestrator agent that coordinates the specialized sub-agents."""
    # Create sub-agents
    transaction_agent = create_transaction_agent()
    relation_agent = create_relation_agent()
    
    # Define the orchestrator agent instruction
    instruction = """
    You are the FinVista Orchestrator Agent, responsible for coordinating financial transaction processing.
    
    Your responsibilities include:
    1. Processing financial transaction requests through the transaction_agent
    2. Managing transaction relationships through the relation_agent
    3. Ensuring data consistency across the system
    4. Routing requests to the appropriate specialized agent
    
    When handling user requests:
    - For transaction operations, delegate to the transaction_agent
    - For relationship operations, delegate to the relation_agent
    - For complex requests requiring both, coordinate between agents as needed
    
    Always respond in a professional, finance-oriented manner.
    """

    # Create the orchestrator agent as a SequentialAgent to manage workflow
    # SequentialAgent in ADK is designed to coordinate multiple sub-agents in sequence
    orchestrator_agent = SequentialAgent(
        name="finvista_orchestrator",
        sub_agents=[transaction_agent, relation_agent],
        description="FinVista orchestrator agent for financial transaction processing",
        instruction=instruction  # Add the instruction to the orchestrator
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
        orchestrator_runner = Runner(
            agent=orchestrator_agent,
            app_name="FinVista",
            # For production, you can implement a session service for state management
            # ADK provides SessionService classes for different storage backends
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
    
    try:
        # Process the request through the orchestrator agent
        # ADK's run_async method handles the message conversion and agent execution
        result = await orchestrator_runner.run_async(request)
        return result
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
