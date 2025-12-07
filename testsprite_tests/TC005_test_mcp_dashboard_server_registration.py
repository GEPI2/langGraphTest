import requests

BASE_URL = "http://localhost:8001"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_mcp_dashboard_server_registration():
    new_server_data = {
        "name": "Test MCP Server",
        "description": "Server registered by automated test",
        "url": "http://test-mcp-server.local",
        "api_key": "testapikey123"
    }

    created_server_id = None

    try:
        # Register new MCP server connection
        response = requests.post(
            f"{BASE_URL}/mcp/servers",
            json=new_server_data,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert response.status_code == 201, f"Expected 201 Created but got {response.status_code}"
        created_server = response.json()
        assert "id" in created_server, "Response JSON must contain 'id'"
        created_server_id = created_server["id"]

        # Verify that the server is listed and stored by the backend
        list_response = requests.get(
            f"{BASE_URL}/mcp/servers",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert list_response.status_code == 200, f"Expected 200 OK but got {list_response.status_code}"
        servers = list_response.json()
        assert any(server["id"] == created_server_id for server in servers), "New server not found in server list"

        # Retrieve the specific server details and verify stored data
        get_response = requests.get(
            f"{BASE_URL}/mcp/servers/{created_server_id}",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert get_response.status_code == 200, f"Expected 200 OK but got {get_response.status_code}"
        server_details = get_response.json()
        assert server_details["name"] == new_server_data["name"], "Server name does not match"
        assert server_details["description"] == new_server_data["description"], "Server description does not match"
        assert server_details["url"] == new_server_data["url"], "Server URL does not match"

    finally:
        # Cleanup: Delete the created MCP server to maintain test environment
        if created_server_id:
            delete_response = requests.delete(
                f"{BASE_URL}/mcp/servers/{created_server_id}",
                headers=HEADERS,
                timeout=TIMEOUT,
            )
            assert delete_response.status_code == 204, f"Expected 204 No Content on delete but got {delete_response.status_code}"

test_mcp_dashboard_server_registration()
