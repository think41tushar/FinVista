from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from integrations.llm.initial_analyser import initialize_pipeline
from integrations.llm.agentic import initialize_agents
from routers import auth, transactions, relations, ai

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initializes the AI agents and pipeline when the server starts."""
    await initialize_pipeline()
    initialize_agents()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Include existing and new routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(relations.router)
app.include_router(ai.router)