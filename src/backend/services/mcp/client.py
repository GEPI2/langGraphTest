from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from src.backend.services.mcp.client_manager import MCPClientManager

router = APIRouter(prefix="/mcp", tags=["mcp"])

# Initialize Manager
manager = MCPClientManager()

class MCPServerConfig(BaseModel):
    name: str
    command: str
    args: List[str] = []
    env: Dict[str, str] = {}

class ToolCallRequest(BaseModel):
    server_name: str
    tool_name: str
    arguments: Dict[str, Any] = {}

@router.post("/servers")
async def connect_server(config: MCPServerConfig):
    try:
        result = await manager.connect_server(config.name, config.command, config.args, config.env)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/servers")
async def list_servers():
    return list(manager.sessions.keys())

@router.get("/tools")
async def list_tools():
    try:
        return await manager.list_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    try:
        result = await manager.call_tool(request.server_name, request.tool_name, request.arguments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
