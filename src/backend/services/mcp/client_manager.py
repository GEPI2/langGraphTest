import asyncio
import os
from typing import Dict, List, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

class MCPClientManager:
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()

    async def connect_server(self, name: str, command: str, args: List[str], env: Dict[str, str] = None):
        """Connects to an MCP server via stdio."""
        if name in self.sessions:
            return {"status": "already_connected", "server": name}

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env={**os.environ, **(env or {})}
        )

        try:
            # Create the client connection
            # Note: In a real long-running app, we need to manage the lifecycle carefully.
            # For this MVP, we'll keep the session open in memory.
            
            # We use the context manager manually to keep it alive
            ctx = stdio_client(server_params)
            read, write = await self.exit_stack.enter_async_context(ctx)
            
            session = ClientSession(read, write)
            await self.exit_stack.enter_async_context(session)
            
            await session.initialize()
            
            self.sessions[name] = session
            return {"status": "connected", "server": name}
        except Exception as e:
            raise Exception(f"Failed to connect to MCP server {name}: {str(e)}")

    async def list_tools(self, server_name: str = None) -> List[Dict[str, Any]]:
        """Lists tools from a specific server or all servers."""
        all_tools = []
        
        targets = [server_name] if server_name else self.sessions.keys()
        
        for name in targets:
            if name not in self.sessions:
                continue
            
            session = self.sessions[name]
            result = await session.list_tools()
            
            for tool in result.tools:
                all_tools.append({
                    "server": name,
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                })
                
        return all_tools

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any] = None):
        """Calls a tool on a specific server."""
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")
            
        session = self.sessions[server_name]
        result = await session.call_tool(tool_name, arguments or {})
        return result
