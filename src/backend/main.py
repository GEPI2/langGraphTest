from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src.backend.engine.schema import GraphConfig
from src.backend.engine.builder import GraphBuilder
from src.backend.engine.meta_agent import MetaAgent
from src.backend.engine.state import AgentState
from src.backend.services.finetune.manager import router as finetune_router
from src.backend.services.rag.manager import router as rag_router
from src.backend.services.mcp.client import router as mcp_router

app = FastAPI(
    title="Dynamic LangGraph Agent API",
    version="2.0",
    description="API for building and executing dynamic LangGraph agents",
)

@app.on_event("startup")
async def startup_event():
    print("Registered Routes:")
    for route in app.routes:
        print(f" - {route.path} [{route.methods}]")

@app.get("/")
async def root():
    return {"message": "Dynamic LangGraph Agent API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(finetune_router)
app.include_router(rag_router)
app.include_router(mcp_router)

# In-memory storage for MVP
graph_configs: Dict[str, GraphConfig] = {}
compiled_graphs: Dict[str, Any] = {}

# Initialize components
builder = GraphBuilder()
meta_agent = MetaAgent()

class ExecuteRequest(BaseModel):
    input: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None

class GenerateNodeRequest(BaseModel):
    description: str

@app.post("/graphs")
async def create_graph(config: GraphConfig):
    """
    Creates or updates a graph configuration and compiles it.
    """
    try:
        # Save config
        graph_configs[config.id] = config
        
        # Build and compile graph
        compiled_app = builder.build_graph(config)
        compiled_graphs[config.id] = compiled_app
        
        return {"status": "success", "graph_id": config.id, "message": "Graph compiled successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/graph/save")
async def create_graph_alias(config: GraphConfig):
    return await create_graph(config)

@app.get("/graphs/{graph_id}")
async def get_graph(graph_id: str):
    """
    Retrieves a graph configuration.
    """
    if graph_id not in graph_configs:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph_configs[graph_id]

@app.post("/graphs/{graph_id}/execute")
async def execute_graph(graph_id: str, request: ExecuteRequest):
    """
    Executes a graph synchronously (for MVP).
    """
    if graph_id not in compiled_graphs:
        raise HTTPException(status_code=404, detail="Graph not found (or not compiled)")
    
    app = compiled_graphs[graph_id]
    
    try:
        print(f"DEBUG: Executing graph {graph_id} with input: {request.input}")
        # Prepare initial state
        initial_state = request.input
        
        # Run graph
        # We use invoke for synchronous execution
        config = request.config or {"configurable": {"thread_id": "default"}}
        result = app.invoke(initial_state, config=config)
        print(f"DEBUG: Execution result: {result}")
        
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/nodes/generate")
async def generate_node_code(request: GenerateNodeRequest):
    """
    Generates Python code for a node based on natural language description.
    """
    try:
        code = meta_agent.generate_node_code(request.description)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
