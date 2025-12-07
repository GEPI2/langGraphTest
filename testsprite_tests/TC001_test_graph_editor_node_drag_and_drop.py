import requests
import uuid

BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_graph_editor_node_drag_and_drop():
    # Simulate drag and drop by creating a graph with nodes
    graph_id = f"test-graph-{uuid.uuid4()}"
    
    # Step 1: Create graph with 2 nodes (Simulate adding nodes)
    graph_config = {
        "id": graph_id,
        "name": "DragDrop Test Graph",
        "nodes": [
            {
                "id": "start-node",
                "type": "StartNode",
                "position": {"x": 0, "y": 0},
                "config": {}
            },
            {
                "id": "node-1",
                "type": "LLMNode",
                "position": {"x": 100, "y": 200},
                "config": {"label": "Node 1", "model": "gpt-4"}
            },
            {
                "id": "node-2",
                "type": "RAGNode",
                "position": {"x": 300, "y": 200},
                "config": {"label": "Node 2", "source": "knowledge_base"}
            }
        ],
        "edges": []
    }
    
    try:
        # Save graph (Create nodes)
        resp1 = requests.post(f"{BASE_URL}/graphs", json=graph_config, headers=HEADERS, timeout=TIMEOUT)
        assert resp1.status_code == 200, f"Failed to save graph with nodes: {resp1.text}"
        
        # Step 2: Add connection (Simulate connecting nodes)
        graph_config["edges"].append({
            "source": "node-1",
            "target": "node-2"
        })
        
        resp2 = requests.post(f"{BASE_URL}/graphs", json=graph_config, headers=HEADERS, timeout=TIMEOUT)
        assert resp2.status_code == 200, f"Failed to save graph with edge: {resp2.text}"
        
        # Verify edge exists
        resp_get = requests.get(f"{BASE_URL}/graphs/{graph_id}", timeout=TIMEOUT)
        assert resp_get.status_code == 200
        saved_graph = resp_get.json()
        assert len(saved_graph["edges"]) == 1
        assert saved_graph["edges"][0]["source"] == "node-1"
        assert saved_graph["edges"][0]["target"] == "node-2"
        
        # Step 3: Delete connection (Simulate removing edge)
        graph_config["edges"] = []
        resp3 = requests.post(f"{BASE_URL}/graphs", json=graph_config, headers=HEADERS, timeout=TIMEOUT)
        assert resp3.status_code == 200, f"Failed to save graph without edge: {resp3.text}"
        
        # Verify edge deleted
        resp_get_after = requests.get(f"{BASE_URL}/graphs/{graph_id}", timeout=TIMEOUT)
        assert resp_get_after.status_code == 200
        saved_graph_after = resp_get_after.json()
        assert len(saved_graph_after["edges"]) == 0
        
    finally:
        # Cleanup is implicit as we don't really delete graphs in MVP, but good practice
        pass

test_graph_editor_node_drag_and_drop()
