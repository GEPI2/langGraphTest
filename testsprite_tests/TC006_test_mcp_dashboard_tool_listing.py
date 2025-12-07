import requests

def test_mcp_dashboard_tool_listing():
    base_url = "http://localhost:8001"
    timeout = 30
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Step 1: Register a new MCP server to ensure at least one server exists
    register_url = f"{base_url}/mcp/servers"
    server_payload = {
        "name": "Test MCP Server",
        "url": "http://test-mcp-server.local",
        "description": "Temporary server for testing tool listing",
        "api_key": "test-api-key",
        "command": "start-server"
    }
    server_id = None

    try:
        register_response = requests.post(register_url, json=server_payload, headers=headers, timeout=timeout)
        assert register_response.status_code == 201, f"Failed to register MCP server: {register_response.text}"
        server_data = register_response.json()
        server_id = server_data.get("id")
        assert server_id is not None, "No server id returned after registration"

        # Step 2: Retrieve the list of available AI tools from the registered MCP servers
        tools_url = f"{base_url}/mcp/servers/{server_id}/tools"
        tools_response = requests.get(tools_url, headers=headers, timeout=timeout)
        assert tools_response.status_code == 200, f"Failed to get tools list: {tools_response.text}"
        tools_list = tools_response.json()

        # Validate that tools_list is a list and contains tool items with expected keys (e.g., name, id)
        assert isinstance(tools_list, list), "Tools response is not a list"
        if len(tools_list) > 0:
            for tool in tools_list:
                assert isinstance(tool, dict), "Each tool should be a dictionary"
                assert "id" in tool, "Tool item missing 'id'"
                assert "name" in tool, "Tool item missing 'name'"

    finally:
        # Cleanup: Delete the MCP server registered for the test if created
        if server_id:
            delete_url = f"{base_url}/mcp/servers/{server_id}"
            try:
                delete_response = requests.delete(delete_url, headers=headers, timeout=timeout)
                assert delete_response.status_code in (200, 204), f"Failed to delete MCP server: {delete_response.text}"
            except Exception:
                pass

test_mcp_dashboard_tool_listing()
