import requests
import time

BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_finetuning_dashboard_job_monitoring():
    create_job_url = f"{BASE_URL}/finetuning/job"
    get_job_status_url_template = f"{BASE_URL}/finetuning/job/{{job_id}}"
    
    # Sample payload for creating a fine-tuning job (fields assumed based on typical fine-tuning jobs)
    create_payload = {
        "model_name": "test-model",
        "training_data": [
            {"input": "Hello", "output": "World"},
            {"input": "Test", "output": "Fine-tuning"}
        ],
        "hyperparameters": {
            "epochs": 1,
            "batch_size": 1,
            "learning_rate": 0.001
        }
    }
    
    job_id = None
    try:
        # Create a new fine-tuning job
        create_response = requests.post(create_job_url, json=create_payload, headers=HEADERS, timeout=TIMEOUT)
        assert create_response.status_code == 201, f"Expected status code 201, got {create_response.status_code}"
        job_data = create_response.json()
        job_id = job_data.get("id")
        assert job_id, "Job ID not returned in create response"
        
        # Poll the job status until it completes or fails, with a max timeout to avoid infinite wait
        max_poll_time = 120  # seconds
        poll_interval = 5    # seconds
        time_spent = 0
        
        while time_spent < max_poll_time:
            status_response = requests.get(get_job_status_url_template.format(job_id=job_id), headers=HEADERS, timeout=TIMEOUT)
            assert status_response.status_code == 200, f"Status check returned {status_response.status_code}"
            status_data = status_response.json()
            
            # Assuming the status_data contains fields 'status' and 'progress' as a percentage 0-100
            status = status_data.get("status")
            progress = status_data.get("progress")
            assert status in {"pending", "running", "completed", "failed"}, f"Invalid status: {status}"
            assert isinstance(progress, (int, float)) and 0 <= progress <= 100, f"Invalid progress value: {progress}"
            
            if status == "completed":
                # Job finished successfully
                break
            if status == "failed":
                assert False, "Fine-tuning job failed during processing"
            
            time.sleep(poll_interval)
            time_spent += poll_interval
        else:
            assert False, "Timeout waiting for fine-tuning job to complete"
            
    finally:
        if job_id:
            # Delete the created job to clean up
            delete_url = f"{BASE_URL}/finetuning/job/{job_id}"
            try:
                del_response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
                assert del_response.status_code in {200, 204, 202}, f"Failed to delete job {job_id}"
            except Exception:
                pass

test_finetuning_dashboard_job_monitoring()
