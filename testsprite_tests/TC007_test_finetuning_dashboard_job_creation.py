import requests

BASE_URL = "http://localhost:8001"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_finetuning_dashboard_job_creation():
    # Adjusted payload to match expected fine-tuning API schema
    payload = {
        "model": "base-model",
        "training_data": [
            {"input": "Translate to French: Hello, world!", "output": "Bonjour le monde!"},
            {"input": "Translate to Spanish: Goodbye!", "output": "¡Adiós!"}
        ],
        "hyperparameters": {
            "epochs": 3,
            "batch_size": 8,
            "learning_rate": 0.0001
        },
        "name": "test-job-finetuning"
    }

    job_id = None
    try:
        # Create a new fine-tuning job
        response = requests.post(
            f"{BASE_URL}/finetune/jobs",
            headers=HEADERS,
            json=payload,
            timeout=TIMEOUT,
        )
        # Assert job creation success status code
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        data = response.json()
        assert "job_id" in data, "Response missing job_id"
        job_id = data["job_id"]
        assert data.get("status") in {"pending", "created"}, "Unexpected job status"

        # Retrieve job details to verify creation
        get_response = requests.get(
            f"{BASE_URL}/finetune/jobs/{job_id}",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert get_response.status_code == 200, f"Expected 200 OK retrieving job, got {get_response.status_code}"
        job_data = get_response.json()

        # Validate returned job data matches what we sent
        assert job_data.get("job_id") == job_id
        assert job_data.get("model") == payload["model"]
        assert job_data.get("name") == payload["name"]
        assert isinstance(job_data.get("training_data"), list)
        assert job_data.get("hyperparameters") == payload["hyperparameters"]
        assert job_data.get("status") in {"pending", "created", "running"}

    finally:
        # Cleanup: delete the created fine-tuning job if it was created
        if job_id:
            try:
                del_response = requests.delete(
                    f"{BASE_URL}/finetune/jobs/{job_id}",
                    headers=HEADERS,
                    timeout=TIMEOUT,
                )
                assert del_response.status_code in {200, 204, 202}, f"Unexpected status deleting job: {del_response.status_code}"
            except Exception:
                pass


test_finetuning_dashboard_job_creation()
