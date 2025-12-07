import requests
import uuid

BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_missing_start_node_fallback():
    graph_id = f"test-graph-fallback-{uuid.uuid4()}"
    
    # Create a graph WITHOUT a StartNode
    graph_payload = {
        "id": graph_id,
        "name": "Fallback Test Graph",
        "nodes": [
            {
                "id": "node-1",
                "type": "CodeNode",
                "config": {
                    "code": "def process(state):\n    return {'messages': ['Fallback worked']}",
                    "function_name": "process"
                }
            }
        ],
        "edges": [] # No edges initially
    }

    try:
        # Create graph
        create_resp = requests.post(
            f"{BASE_URL}/graphs",
            json=graph_payload,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert create_resp.status_code == 200, f"Graph creation failed: {create_resp.text}"
        
        # Execute graph
        # If fallback works, START should be connected to node-1
        execute_payload = {
            "input": {"messages": []}
        }
        
        execute_resp = requests.post(
            f"{BASE_URL}/graphs/{graph_id}/execute",
            json=execute_payload,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert execute_resp.status_code == 200, f"Graph execution failed: {execute_resp.text}"
        
        result = execute_resp.json()
        
        # Check result
        messages = result.get("messages", [])
        found = False
        for msg in messages:
            if isinstance(msg, dict) and msg.get("content") == "Fallback worked":
                found = True
                break
            elif isinstance(msg, str) and msg == "Fallback worked":
                found = True
                break
        assert found, f"Expected message not found in result: {result}"
        print("TC011 Passed: Fallback logic works.")

    finally:
        pass

if __name__ == "__main__":
    test_missing_start_node_fallback()
