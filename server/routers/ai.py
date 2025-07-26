from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from integrations.llm.agentic import process_request
from integrations.llm.initial_analyser import initialize_pipeline, runner as initial_pipeline_runner

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)

class QueryRequest(BaseModel):
    query: str

@router.post("/run-initial-pipeline")
async def run_initial_pipeline():
    """Endpoint to trigger the initial data cleaning and tagging pipeline."""
    try:
        await initialize_pipeline()
        if not initial_pipeline_runner:
            raise HTTPException(status_code=500, detail="Initial pipeline runner not available.")
        result = await initial_pipeline_runner.run_async("Start initial data processing")
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_agent(request: QueryRequest):
    """Endpoint to process a user query through the main FinVista agent."""
    try:
        response = await process_request(request.query)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
