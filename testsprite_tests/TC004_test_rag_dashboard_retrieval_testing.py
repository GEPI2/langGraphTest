import requests
from io import BytesIO

BASE_URL = "http://localhost:8001"
TIMEOUT = 30

def test_rag_dashboard_retrieval_testing():
    # Step 1: Upload a sample document to create a knowledge base entry
    upload_url = f"{BASE_URL}/rag/upload"
    retrieval_url = f"{BASE_URL}/rag/retrieve"

    # Using multipart/form-data upload with a file field named 'file'
    file_content = b"LangGraph Builder allows users to create complex AI agent workflows using a visual editor."
    files = {"file": ("sample.txt", BytesIO(file_content), "text/plain")}

    # Upload the document
    upload_resp = requests.post(upload_url, files=files, timeout=TIMEOUT)
    assert upload_resp.status_code == 200, f"Document upload failed: {upload_resp.status_code} {upload_resp.text}"
    upload_data = upload_resp.json()
    assert upload_data.get("success") is True or upload_data.get("status") == "ok", "Upload response missing success status"

    # Step 2: Test retrieval of information related to the uploaded document
    query_payload = {
        "query": "What does the LangGraph Builder allow users to do?"
    }

    retrieval_resp = requests.post(retrieval_url, json=query_payload, timeout=TIMEOUT)
    assert retrieval_resp.status_code == 200, f"Retrieval request failed: {retrieval_resp.status_code} {retrieval_resp.text}"
    retrieval_data = retrieval_resp.json()

    # Validate that retrieval response contains expected text or relevant info
    assert "answer" in retrieval_data or "results" in retrieval_data, "Retrieval response missing expected keys"

    # If 'answer' is available, check if it contains relevant info
    if "answer" in retrieval_data:
        answer = retrieval_data["answer"]
        assert "LangGraph Builder" in answer or "AI agent workflows" in answer, "Answer doesn't contain expected content"
    elif "results" in retrieval_data and isinstance(retrieval_data["results"], list):
        text_found = any("LangGraph Builder" in str(result) or "AI agent workflows" in str(result) for result in retrieval_data["results"])
        assert text_found, "Results do not contain expected content"
    else:
        assert False, "Retrieval response format not recognized"

# Run the test

test_rag_dashboard_retrieval_testing()