import requests
import json
import sseclient  # You might need to install this: pip install sseclient-py

def verify_stream():
    url = "http://localhost:8000/agent/stream_events"
    payload = {
        "input": {"messages": [{"role": "user", "content": "안녕"}]},
        "config": {"configurable": {"thread_id": "test_thread_1"}},
        "version": "v2"
    }
    
    print(f"Connecting to {url}...")
    headers = {"X-Thread-Id": "test_thread_1"}
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        client = sseclient.SSEClient(response)
        for event in client.events():
            print(f"Event: {event.event}")
            print(f"Data: {event.data[:100]}...") # Truncate data for readability
            
            if event.event == "on_chat_model_stream":
                data = json.loads(event.data)
                chunk = data.get("chunk", {})
                content = chunk.get("content", "")
                if content:
                    print(f"Content: {content}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_stream()
