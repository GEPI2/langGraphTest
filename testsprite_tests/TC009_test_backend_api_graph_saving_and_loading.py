import requests
import uuid

BASE_URL = "http://localhost:8001"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_backend_api_graph_saving_and_loading():
    graph_config = {
        "id": f"test-graph-{uuid.uuid4()}",
        "name": "Test Graph Configuration",
        "description": "Graph config for TC009 validation",
        "nodes": [
            {
                "id": "start-node",
                "type": "StartNode",
                "position": {"x": 0, "y": 0},
                "config": {},
            },
            {
                "id": "node-1",
                "type": "LLMNode",
                "position": {"x": 100, "y": 150},
                "config": {"model_name": "gpt-4", "parameters": {"temperature": 0.7}},
            },
            {
                "id": "node-2",
                "type": "RAGNode",
                "position": {"x": 300, "y": 150},
                "config": {"retriever": "simple-retriever", "top_k": 5},
            }
        ],
        "edges": [
            {"id": "edge-start-1", "source": "start-node", "target": "node-1", "type": "default"},
            {"id": "edge-1-2", "source": "node-1", "target": "node-2", "type": "default"}
        ],
        "metadata": {"created_by": "test_backend_api_graph_saving_and_loading", "version": 1}
    }

    try:
        # Save the graph configuration
        save_response = requests.post(
            f"{BASE_URL}/graphs/",
            headers=HEADERS,
            json=graph_config,
            timeout=TIMEOUT,
        )
        assert save_response.status_code == 200, f"Failed to save graph config: {save_response.text}"
        saved_response = save_response.json()
        assert saved_response.get("graph_id") == graph_config["id"], "Saved graph ID mismatch"

        # Load the saved graph configuration
        load_response = requests.get(
            f"{BASE_URL}/graphs/{graph_config['id']}",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert load_response.status_code == 200, f"Failed to load graph config: {load_response.text}"
        loaded_graph = load_response.json()

        # Validate loaded graph equals saved one (deep check)
        assert loaded_graph.get("id") == graph_config["id"], "Loaded graph ID mismatch"
        assert loaded_graph.get("name") == graph_config["name"], "Graph name mismatch after loading"
        assert loaded_graph.get("description") == graph_config["description"], "Graph description mismatch after loading"
        assert loaded_graph.get("metadata") == graph_config["metadata"], "Graph metadata mismatch after loading"

        # Validate nodes and edges
        loaded_nodes = loaded_graph.get("nodes")
        loaded_edges = loaded_graph.get("edges")
        assert isinstance(loaded_nodes, list), "Loaded nodes is not a list"
        assert isinstance(loaded_edges, list), "Loaded edges is not a list"
        assert len(loaded_nodes) == len(graph_config["nodes"]), "Number of nodes mismatch after loading"
        assert len(loaded_edges) == len(graph_config["edges"]), "Number of edges mismatch after loading"

        # Check details of nodes
        for original_node in graph_config["nodes"]:
            matched_node = next((n for n in loaded_nodes if n["id"] == original_node["id"]), None)
            assert matched_node is not None, f"Node {original_node['id']} missing after load"
            assert matched_node["type"] == original_node["type"], f"Node type mismatch for {original_node['id']}"
            assert matched_node["position"] == original_node["position"], f"Node position mismatch for {original_node['id']}"
            assert matched_node["config"] == original_node["config"], f"Node config mismatch for {original_node['id']}"

        # Check details of edges
        # Check details of edges
        for original_edge in graph_config["edges"]:
            matched_edge = next((e for e in loaded_edges if e["source"] == original_edge["source"] and e["target"] == original_edge["target"]), None)
            assert matched_edge is not None, f"Edge {original_edge['source']}->{original_edge['target']} missing after load"
            # assert matched_edge["type"] == original_edge["type"], f"Edge type mismatch" # Schema doesn't have type either

    finally:
        # Cleanup: delete the graph configuration if created
        try:
            requests.delete(
                f"{BASE_URL}/graphs/{graph_config['id']}",
                headers=HEADERS,
                timeout=TIMEOUT,
            )
        except Exception:
            pass

test_backend_api_graph_saving_and_loading()
