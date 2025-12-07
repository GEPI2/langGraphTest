import requests

BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_backend_api_error_handling_for_invalid_inputs():
    """
    Verify that the backend API handles invalid user inputs gracefully by returning appropriate error messages
    and preventing faulty states in the system.
    The test tries to send invalid inputs to various endpoints to check error handling.
    """

    # List of endpoint tests with method, url path, and invalid payloads or parameters
    tests = [
        # Graph save with invalid payload (missing required fields)
        {
            "method": "POST",
            "url": "/graph/save",
            "json": {"invalidField": 123},
            "expected_status": 422
        },
        # Execute graph with invalid body
        {
            "method": "POST",
            "url": "/graphs/some-id/execute",
            "json": {"invalidField": "not_valid"},
            "expected_status": 422
        },
        # RAG document upload with invalid file data (missing required file content)
        {
            "method": "POST",
            "url": "/rag/upload",
            "json": {"filename": "", "content": ""},
            "expected_status": 422
        },
        # MCP server registration with invalid connection string format
        {
            "method": "POST",
            "url": "/mcp/servers",
            "json": {"serverName": "", "connectionString": "invalid-url"},
            "expected_status": 422
        },
        # Fine-tuning job creation with missing parameters
        {
            "method": "POST",
            "url": "/finetune/jobs",
            "json": {"model": "", "trainingData": None},
            "expected_status": 422
        },
        # Invalid HTTP method on a valid endpoint
        {
            "method": "PUT",
            "url": "/graph/save",
            "json": {},
            "expected_status": 405
        },
        # Invalid route
        {
            "method": "GET",
            "url": "/nonexistent/endpoint",
            "json": None,
            "expected_status": 404
        }
    ]

    for test_case in tests:
        method = test_case["method"].lower()
        url = BASE_URL + test_case["url"]
        json_data = test_case["json"]
        expected_status = test_case["expected_status"]

        try:
            if method == "get":
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            elif method == "post":
                response = requests.post(url, headers=HEADERS, json=json_data, timeout=TIMEOUT)
            elif method == "put":
                response = requests.put(url, headers=HEADERS, json=json_data, timeout=TIMEOUT)
            elif method == "delete":
                response = requests.delete(url, headers=HEADERS, json=json_data, timeout=TIMEOUT)
            else:
                # Unsupported method for this test - skip
                continue
        except requests.RequestException as e:
            assert False, f"Request to {url} with method {method} failed unexpectedly: {str(e)}"

        assert response.status_code == expected_status, (
            f"Expected status {expected_status} but got {response.status_code} "
            f"for {method.upper()} {url} with payload {json_data}. "
            f"Response body: {response.text}"
        )

        # For error responses, check error message presence
        if expected_status >= 400:
            try:
                data = response.json()
                assert ("detail" in data) or ("error" in data) or ("message" in data), \
                    f"Error response missing expected keys in JSON body for {url}: {data}"
            except Exception:
                # If response not JSON, ensure something meaningful is returned instead of empty
                assert len(response.text) > 0, f"Empty error response body for {url}"

test_backend_api_error_handling_for_invalid_inputs()