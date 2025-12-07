import requests
import uuid

BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_graph_execution_trigger():
    graph_id = f"test-graph-{uuid.uuid4()}"
    
    # Create a simple graph that just returns a value
    graph_payload = {
        "id": graph_id,
        "name": "Execution Test Graph",
        "nodes": [
            {
                "id": "start-node",
                "type": "StartNode",
                "config": {}
            },
            {
                "id": "node-1",
                "type": "CodeNode",
                "config": {
                    "code": "def process(state):\n    return {'messages': ['Hello from CodeNode']}",
                    "function_name": "process"
                }
            }
        ],
        "edges": [
            # StartNode is automatically connected to START by builder
            # But we need to connect StartNode to Node 1
            {"source": "start-node", "target": "node-1"}
        ]
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
        # Input state is required
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
        # Check if result contains the expected output from CodeNode
        # The result is the final state. CodeNode adds to messages.
        # But wait, CodeNode in my factory returns the result directly.
        # And LangGraph updates state.
        # If CodeNode returns {'messages': ...}, it updates the messages key in state.
        assert "messages" in result, "Result missing messages"
        # Check if any message has the expected content
        messages = result["messages"]
        found = False
        for msg in messages:
            if isinstance(msg, dict) and msg.get("content") == "Hello from CodeNode":
                found = True
                break
            elif isinstance(msg, str) and msg == "Hello from CodeNode":
                found = True
                break
        assert found, f"Expected message not found in result: {result}"

    finally:
        pass

test_graph_execution_trigger()
