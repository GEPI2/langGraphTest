import docker
import os
import time
import uuid

# 공유 볼륨 경로 (컨테이너 내부 기준)
SANDBOX_DIR = "/app/sandbox_data"

def run_in_sandbox(code: str, timeout: int = 30) -> str:
    """
    Executes Python code in a secure Docker container using a shared volume.
    """
    client = docker.from_env()
    
    # Ensure sandbox directory exists
    os.makedirs(SANDBOX_DIR, exist_ok=True)

    # Create a unique file for the code
    filename = f"script_{uuid.uuid4().hex}.py"
    host_path = os.path.join(SANDBOX_DIR, filename)
    
    with open(host_path, 'w', encoding='utf-8') as f:
        f.write(code)

    try:
        # Run the container
        # Mount the shared volume 'sandbox-data' to /app/sandbox_data in the sandbox container
        # Note: When using DooD, the volume name 'langgraphtest_sandbox-data' (project_name + volume_name) 
        # is usually required, but mounting by volume name is cleaner.
        # However, since we are inside a container, we need to know how the host sees this volume.
        # A simpler approach for DooD is to use 'volumes_from' if possible, but python-docker client uses 'volumes'.
        # Let's try mounting the named volume directly.
        
        # IMPORTANT: The volume name depends on the docker-compose project name.
        # Default is directory name 'langgraphtest'.
        volume_name = "langgraphtest_sandbox-data" 

        container = client.containers.run(
            "python:3.10-slim",
            command=f"python /sandbox/{filename}",
            volumes={volume_name: {'bind': '/sandbox', 'mode': 'ro'}},
            working_dir="/sandbox",
            detach=True,
            mem_limit="128m",
            cpu_period=100000,
            cpu_quota=50000,
            network_disabled=True
        )

        # Wait for result or timeout
        exit_code = container.wait(timeout=timeout)
        logs = container.logs().decode('utf-8')
        
        if exit_code['StatusCode'] != 0:
            return f"Error (Exit Code {exit_code['StatusCode']}):\n{logs}"
        
        return logs

    except Exception as e:
        return f"Sandbox Error: {str(e)}"
    finally:
        # Cleanup container
        try:
            container.remove(force=True)
        except:
            pass
        # Cleanup file
        if os.path.exists(host_path):
            os.remove(host_path)

if __name__ == "__main__":
    # Test
    print(run_in_sandbox("print('Hello from Sandbox')"))
