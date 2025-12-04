import docker
import os
import tempfile
import time

def run_in_sandbox(code: str, timeout: int = 30) -> str:
    """
    Executes Python code in a secure Docker container.
    """
    client = docker.from_env()
    
    # Create a temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        host_path = f.name
        filename = os.path.basename(host_path)

    try:
        # Run the container
        # Mount the temp file to /app/script.py
        # Use python:3.10-slim for a lightweight environment
        container = client.containers.run(
            "python:3.10-slim",
            command=f"python /app/{filename}",
            volumes={os.path.dirname(host_path): {'bind': '/app', 'mode': 'ro'}},
            working_dir="/app",
            detach=True,
            mem_limit="128m",  # Limit memory
            cpu_period=100000,
            cpu_quota=50000,   # Limit CPU (50%)
            network_disabled=True # Disable network for security
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
        # Cleanup
        try:
            container.remove(force=True)
        except:
            pass
        if os.path.exists(host_path):
            os.remove(host_path)

if __name__ == "__main__":
    # Test
    print(run_in_sandbox("print('Hello from Sandbox')"))
