from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from integrations.llm.agentic import process_request
from integrations.llm.initial_analyser import initialize_pipeline, runner
from integrations.llm.agentic import logger

# Import new GenAI SDK
from google import genai
from google.genai import types


router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)


class QueryRequest(BaseModel):
    query: str
    user_id: str = None  # Make user_id optional for backward compatibility


@router.post("/run-initial-pipeline")
async def run_initial_pipeline():
    """Endpoint to trigger the initial data cleaning and tagging pipeline."""
    try:
        # Initialize the pipeline runner and session
        current_runner, session = await initialize_pipeline()
        if not current_runner or not session:
            raise HTTPException(status_code=500, detail="Initial pipeline runner or session not available.")
        
        # Construct the user content using new GenAI SDK types
        user_content = types.UserContent(
            parts=[
                types.Part.from_text(text="Start the initial data processing")
            ]
        )

        
        # Call the async run method of your runner with proper arguments
        async_gen = current_runner.run_async(
            user_id=session.user_id,   # Pass user ID from session
            session_id=session.id,     # Pass session ID from session object
            new_message=user_content   # Use UserContent instance
        )
        
        # Collect assistant responses
        responses = []
        async for event in async_gen:
            logger.info(f"Received event type: {type(event).__name__}")
            
            # Depending on event structure, extract content from assistant responses
            if hasattr(event, 'role') and event.role == 'assistant' and hasattr(event, 'content'):
                if event.content:
                    # Append content string directly
                    if isinstance(event.content, str):
                        responses.append(event.content)
                    else:
                        # Sometimes content might be complex; convert to string
                        responses.append(str(event.content))
            elif hasattr(event, 'content') and event.content:
                responses.append(str(event.content))
        
        result = "\n".join(responses) if responses else "Pipeline completed with no output"
        
        return {"status": "success", "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def query_agent(request: QueryRequest):
    """Endpoint to process a user query through the main FinVista agent."""
    try:
        response = await process_request(request.query, request.user_id)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
