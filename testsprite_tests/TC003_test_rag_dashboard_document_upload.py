import requests
import os

BASE_URL = "http://localhost:8001"
TIMEOUT = 30

def test_rag_dashboard_document_upload():
    upload_url = f"{BASE_URL}/rag/upload"
    
    file_content = b"Sample content for RAG knowledge base document upload test."
    files = {
        'file': ('test_document.txt', file_content, 'text/plain')
    }
    
    try:
        response = requests.post(upload_url, files=files, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to upload document failed: {e}"
    
    assert response.status_code in (200, 201), f"Unexpected status code: {response.status_code}, response: {response.text}"
    
    try:
        resp_json = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"
    
    assert ('filename' in resp_json and 'status' in resp_json), \
        f"Response JSON missing expected keys: {resp_json}"
    
    if response.status_code not in (200, 201):
        assert 'error' in resp_json or 'detail' in resp_json, f"Expected error details in response: {resp_json}"

test_rag_dashboard_document_upload()
