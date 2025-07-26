from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from integrations.llm.initial_analyser import initialize_pipeline
from integrations.llm.agentic import initialize_agents
from routers import auth, transactions, relations, spendings, ai

# Load environment variables from .env file
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

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

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(relations.router)
app.include_router(spendings.router)
app.include_router(ai.router)